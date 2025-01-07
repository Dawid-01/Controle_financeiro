from django.shortcuts import render, redirect
from .models import Expense, Income
from .forms import ExpenseForm, IncomeForm
from django.http import HttpResponse
import xlsxwriter

def index(request):
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    total_expenses = sum(exp.amount for exp in expenses)
    total_income = sum(inc.amount for inc in incomes)
    return render(request, 'finance/index.html', {
        'expenses': expenses,
        'incomes': incomes,
        'total_expenses': total_expenses,
        'total_income': total_income,
    })

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ExpenseForm()
    return render(request, 'finance/add_expense.html', {'form': form})

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = IncomeForm()
    return render(request, 'finance/add_income.html', {'form': form})

def generate_report(request):
    expenses = Expense.objects.all()
    incomes = Income.objects.all()

    # Criar arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    sheet = workbook.add_worksheet()

    # Cabeçalhos
    sheet.write(0, 0, 'Descrição')
    sheet.write(0, 1, 'Valor')
    sheet.write(0, 2, 'Data de Vencimento')
    sheet.write(0, 3, 'Pago')
    sheet.write(0, 4, 'Atrasado')

    # Dados de despesas
    for row_num, expense in enumerate(expenses, start=1):
        sheet.write(row_num, 0, expense.description)
        sheet.write(row_num, 1, str(expense.amount))
        sheet.write(row_num, 2, expense.due_date.strftime('%Y-%m-%d'))
        sheet.write(row_num, 3, 'Sim' if expense.is_paid else 'Não')
        sheet.write(row_num, 4, 'Sim' if expense.is_late else 'Não')

    workbook.close()
    return response
