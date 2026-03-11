from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .forms import TransactionUploadForm
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.db.models import Sum
from decimal import Decimal

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    
    # Simple summary stats
    total_spend = transactions.aggregate(total=Sum('amount'))['total'] or 0
    
    # Charts
    chart_pie = ""
    chart_line = ""
    
    if transactions.exists():
        # Chart 1: Spend by Category
        category_data = transactions.values('category__name').annotate(total=Sum('amount'))
        cat_names = [d['category__name'] or 'Uncategorized' for d in category_data]
        cat_totals = [float(d['total'] or 0) for d in category_data]
        
        # Calculate Top Category
        top_cat_name = "None"
        if category_data:
            top_cat_item = max(category_data, key=lambda x: x['total'] or 0)
            top_cat_name = top_cat_item['category__name'] or "Uncategorized"
        
        if cat_names:
            fig_pie = px.pie(names=cat_names, values=cat_totals, title="Spending by Category",
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

        # Chart 2: Spend over Time
        time_data = transactions.values('date').annotate(total=Sum('amount')).order_by('date')
        dates = [d['date'] for d in time_data]
        amounts = [float(d['total'] or 0) for d in time_data]
        
        if dates:
            fig_line = px.line(x=dates, y=amounts, title="Spending Trend", template="plotly_dark")
            fig_line.update_layout(
                autosize=True,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font_color="white",
                margin=dict(l=10, r=10, t=50, b=10),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            chart_line = fig_line.to_html(full_html=False, config={'responsive': True, 'displayModeBar': False})

    context = {
        'total_spend': total_spend,
        'top_category': top_cat_name if transactions.exists() else "None",
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
