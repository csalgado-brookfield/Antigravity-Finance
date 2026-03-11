from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .forms import TransactionUploadForm
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    
    # Date logic for MoM
    today = timezone.now().date()
    # For testing/demo purposes, if there's no data today, we might want to use the latest transaction date
    if not transactions.exists():
        latest_date = today
    else:
        latest_date = transactions.latest('date').date
    
    first_day_this_month = latest_date.replace(day=1)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)

    # Aggregations
    total_spend = transactions.filter(date__gte=first_day_this_month).aggregate(total=Sum('amount'))['total'] or 0
    prev_total_spend = transactions.filter(date__gte=first_day_prev_month, date__lte=last_day_prev_month).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate % Change
    if prev_total_spend > 0:
        percent_change = ((total_spend - prev_total_spend) / prev_total_spend) * 100
    else:
        percent_change = 0

    # Charts
    chart_pie = ""
    chart_line = ""
    top_cat_name = "None"
    
    if transactions.exists():
        # Chart 1: Spend by Category (Current Month)
        category_data = transactions.filter(date__gte=first_day_this_month).values('category__name').annotate(total=Sum('amount'))
        cat_names = [d['category__name'] or 'Uncategorized' for d in category_data]
        cat_totals = [float(d['total'] or 0) for d in category_data]
        
        if category_data:
            top_cat_item = max(category_data, key=lambda x: x['total'] or 0)
            top_cat_name = top_cat_item['category__name'] or "Uncategorized"
        
        if cat_names:
            fig_pie = px.pie(names=cat_names, values=cat_totals, title="Spend by Category",
                            color_discrete_sequence=px.colors.sequential.RdBu,
                            template="plotly_dark")
            fig_pie.update_layout(
                autosize=True,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font_color="white",
                margin=dict(l=10, r=10, t=50, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            chart_pie = fig_pie.to_html(full_html=False, config={'responsive': True, 'displayModeBar': False})

        # Chart 2: MoM Comparison Line Chart
        # Current Month Data
        current_data = transactions.filter(date__gte=first_day_this_month).values('date').annotate(total=Sum('amount')).order_by('date')
        # Prev Month Data
        prev_data = transactions.filter(date__gte=first_day_prev_month, date__lte=last_day_prev_month).values('date').annotate(total=Sum('amount')).order_by('date')
        
        fig_mom = go.Figure()
        
        # Current Month Line
        if current_data:
            # Re-index to day of month (1-31)
            curr_days = [d['date'].day for d in current_data]
            curr_vals = [float(d['total']) for d in current_data]
            fig_mom.add_trace(go.Scatter(x=curr_days, y=curr_vals, name="This Month", line=dict(color='#bb86fc', width=3)))
            
        # Prev Month Line
        if prev_data:
            prev_days = [d['date'].day for d in prev_data]
            prev_vals = [float(d['total']) for d in prev_data]
            fig_mom.add_trace(go.Scatter(x=prev_days, y=prev_vals, name="Last Month", line=dict(color='rgba(255,255,255,0.3)', width=2, dash='dot')))

        fig_mom.update_layout(
            title="Today vs. Last Month",
            template="plotly_dark",
            autosize=True,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color="white",
            margin=dict(l=10, r=10, t=50, b=10),
            xaxis=dict(title="Day of Month", showgrid=False),
            yaxis=dict(title="Spend ($)", showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        chart_line = fig_mom.to_html(full_html=False, config={'responsive': True, 'displayModeBar': False})

    context = {
        'total_spend': total_spend,
        'prev_total_spend': prev_total_spend,
        'percent_change': percent_change,
        'top_category': top_cat_name,
        'chart_pie': chart_pie,
        'chart_line': chart_line,
        'recent_transactions': transactions.order_by('-date')[:10],
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = TransactionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)
            
            # Basic mapping logic (Assumes headers: Date, Description, Amount)
            # You might need to adjust these based on your specific CSV
            for index, row in df.iterrows():
                # Attempt to find common column names
                date_str = row.get('Date') or row.get('Transaction Date')
                desc = row.get('Description') or row.get('Merchant')
                amount = row.get('Amount') or row.get('Debit')
                
                if date_str and desc and amount:
                    # Simple cleaning
                    try:
                        amt = Decimal(str(amount).replace('$', '').replace(',', ''))
                        # Auto-categorization logic
                        cat = auto_categorize(desc)
                        
                        Transaction.objects.create(
                            user=request.user,
                            date=pd.to_datetime(date_str).date(),
                            description=desc,
                            amount=amt,
                            category=cat,
                            source_file=csv_file.name
                        )
                    except Exception as e:
                        print(f"Error processing row {index}: {e}")
            
            return redirect('dashboard')
    else:
        form = TransactionUploadForm()
    return render(request, 'tracker/upload.html', {'form': form})

def auto_categorize(description):
    desc = description.lower()
    mapping = {
        'Food': ['restaurant', 'mcdonalds', 'starbucks', 'uber eats', 'grocery', 'walmart', 'kroger', 'whole foods'],
        'Transport': ['uber', 'lyft', 'shell', 'exxon', 'gas', 'transit', 'train'],
        'Entertainment': ['netflix', 'spotify', 'hulu', 'theater', 'cinema', 'game'],
        'Utilities': ['electric', 'water', 'internet', 'comcast', 'att', 'verizon'],
        'Rent/Home': ['rent', 'mortgage', 'home depot', 'lowes', 'ikea'],
    }
    
    for cat_name, keywords in mapping.items():
        if any(k in desc for k in keywords):
            category, created = Category.objects.get_or_create(name=cat_name)
            return category
    
    return None

@login_required
def list_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.all()
    
    if request.method == 'POST':
        tx_id = request.POST.get('tx_id')
        cat_id = request.POST.get('category_id')
        transaction = Transaction.objects.get(id=tx_id, user=request.user)
        category = Category.objects.get(id=cat_id)
        transaction.category = category
        transaction.save()
        return redirect('list_transactions')

    return render(request, 'tracker/transactions.html', {'transactions': transactions, 'categories': categories})
