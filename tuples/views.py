# Create your views here.
from datetime import date, datetime
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from forms import *
from models import *

def account(request):
    form = AccountForm()
    parent_account_high = Account.objects.filter(account_level='High')
    parent_account_medium = Account.objects.filter(account_level='Medium')
    
    if request.method=='POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("data saved")
        else:
            return render_to_response('errors.html',{'form':form},RequestContext(request))
    else:
        return render_to_response('account.html',{'parent_account_medium':parent_account_medium,'parent_account_high':parent_account_high,'form':form},RequestContext(request))

def edit_account(request):
    account = Account.objects.all()
    form = AccountForm()
    if request.method == 'POST':
        if 'update' in request.POST:
            account_number = request.POST['account_number']
            name = request.POST['account_name']
            start_date = request.POST['account_start_date']
            end_date = request.POST['account_end_date']
            status = request.POST['status']
            Account.objects.filter(account_number=account_number).update(updated_date=datetime.now(),status=status,account_name=name,account_start_date=start_date,account_end_date=end_date)
            return HttpResponse("data updated")
        else:
            account_number = request.POST['parent_account_number']
            all_types = account_type.objects.all()
            status = Status.objects.all()
            account = Account.objects.get(account_number=account_number)
            level = account.account_level
            current_account_type= account.account_type
            form = AccountForm(request.POST,instance=account)
            if (level=='High'):
                return render_to_response('edit_account_id.html',{'status':status,'all_types':all_types,'account_type':current_account_type,'account':account,'form':form},RequestContext(request))
            else:
                if(level=='Medium'):
                    parent_account = Account.objects.filter(account_level='High')
                    print parent_account,account
                    return render_to_response('edit_account_id.html',{'parent_account_list':parent_account,'status':status,'all_types':all_types,'account_type':current_account_type,'account':account,'form':form},RequestContext(request))
                else:
                    parent_account = Account.objects.filter(account_level='Medium')
                    return render_to_response('edit_account_id.html',{'parent_account_list':parent_account,'status':status,'all_types':all_types,'account_type':current_account_type,'account':account,'form':form},RequestContext(request))
               
#        if form.is_valid():
#            form.save()
#            print "saved"
#            
#        else:
#            return render_to_response('errors.html',{'form':form},RequestContext(request))
#    else:
    return render_to_response('edit_account.html',{'account':account,'form':form},RequestContext(request))

     
def sub_account(request):
    form = Sub_AccountForm()
    datee = date.today()
    parent_account_low = Account.objects.filter(account_level='Low')
    if request.method=='POST':
        form = Sub_AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("data saved")
        else:
            return render_to_response('errors.html',{'form':form},RequestContext(request))
    else:
        return render_to_response('sub_account.html',{'date':datee,'parent_account_low':parent_account_low,'form':form},RequestContext(request))
    
def manage_account(request):
    account_list_high = Account.objects.filter(account_level='High')
    account_list_medium = Account.objects.filter(account_level='Medium')
    account_list_low = Account.objects.filter(account_level='Low')
    return render_to_response('manage.html',{'account_list_high':account_list_high,'account_list_medium':account_list_medium,'account_list_low':account_list_low},RequestContext(request))


def budget(request):
    account = Account.objects.all()
    parent_acc_list =[]
    for a_n in account:
        parent_acc_list.append(a_n.parent_account)
    if request.method=='POST':
        if 'save' in request.POST:
            bud = Budget.objects.all()
            for x in bud:
                try:
                    amnt = request.POST[str(x.id)]
                    print amnt
                    print x.id,request.POST[str(x.id)]
                    Budget.objects.filter(id=x.id).update(amount=amnt)
                except:
                    pass
            return HttpResponse("Page Under Construction")
        if 'go' in request.POST:
            account_number = request.POST['account_number']
            account_period = request.POST['account_period']
            acc = Account.objects.get(account_number=account_number)
            for i in range(1,13):
                print i
                try:
                    Budget.objects.get(account=acc,year=account_period,month=i)
                    pass
                except:
                    Budget.objects.create(account=acc,year=account_period,month=i,amount=0)
                    pass
            year = " "+account_period[-2:]
            account_object = Account.objects.get(account_number=account_number)
            level = account_object.account_level
            budget_amount = Budget.objects.filter(year=account_period)
            if level == "High" and account_object.account_number in parent_acc_list:
                medium_accounts = Account.objects.filter(parent_account=account_number)
                for m_a in medium_accounts:
                    acc= Account.objects.get(account_number=m_a.account_number)
                    for i in range(1,13):
                        try:
                            Budget.objects.get(account=acc,year=account_period,month=i)
                            pass
                        except:
                            Budget.objects.create(account=acc,year=account_period,month=i,amount=0)
                        pass
                low_accounts = Account.objects.filter(account_level="Low")
                for l_a in low_accounts:
                    acc= Account.objects.get(account_number=l_a.account_number)
                    for i in range(1,13):
                        try:
                            Budget.objects.get(account=acc,year=account_period,month=i)
                            pass
                        except:
                            Budget.objects.create(account=acc,year=account_period,month=i,amount=0)
                        pass
                return render_to_response('budget.html',{'b_a':budget_amount,'low_accounts':low_accounts,'medium_accounts':medium_accounts,'selected_account':account_object,'year':year,'account':account},RequestContext(request))
    return render_to_response('budget.html',{'account':account},RequestContext(request))

def budget1(request):
    account = Account.objects.all()
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    if request.method=='POST':
#        if 'save' in request.POST:
#            g = Budget1.objects.filter(accounting_period__year__contains=request.POST['account_period'])
#            acc_list=Account.objects.filter(account_level=str("Medium"),parent_account=request.POST['account_number'])
#            for bud in g:
#                try:
#                    amount = request.POST[str(bud.id)]
#                    Budget1.objects.filter(id=bud.id).update(amount=amount)
#                    for acc in acc_list:
#                        acc_low = Account.objects.filter(parent_account=acc.account_number)
#                        i=0
#                        for acc_l in acc_low:
#                            budget_amount = Budget1.objects.get(account=acc_l,accounting_period=bud.accounting_period)
#                            i=i+budget_amount.amount
#                        Budget1.objects.filter(account=acc,accounting_period=bud.accounting_period).update(amount=i)
#                    acc = Account.objects.get(account_number=request.POST['account_number'])
#                    acc_med = Account.objects.filter(parent_account=request.POST['account_number']) 
#                    i=0
#                    for acc_m in acc_med:
#                        budget_amount = Budget1.objects.get(account=acc_m,accounting_period=bud.accounting_period)
#                        i=i+budget_amount.amount
#                    Budget1.objects.filter(account=acc,accounting_period=bud.accounting_period).update(amount=i)
#                except:
#                    pass
#            account_number = request.POST['account_number']
#            account_period = request.POST['account_period']
#            for x in range(1,13):
#                if accounting_period.objects.filter(month=x,year=account_period).count() == 0:
#                    accounting_period.objects.create(month=x,year=account_period)
#                else:
#                    pass
#            acc_period = accounting_period.objects.filter(year=account_period)
#            acc = Account.objects.get(account_number=account_number)
#            year = " "+account_period[-2:]
#            account_object = Account.objects.get(account_number=account_number)
#            level = account_object.account_level
#            if level == "High":
#                medium_accounts = Account.objects.filter(parent_account=account_number)
#                low_accounts = Account.objects.filter(account_level="Low")
#                budget = Budget1.objects.all()
#                return render_to_response('budget1.html',{'current_year':current_year,'current_month':current_month,'z':int(account_period),'acc_period':acc_period,'budget':budget,'year_f':account_period,'low_accounts':low_accounts,'medium_accounts':medium_accounts,'mm':account_object.account_number,'selected_account':account_object,'year':year,'account':account},RequestContext(request))
        if 'go' in request.POST:
            p_d_o = request.POST['p_d_o']# post data option
            if p_d_o == "1":
                account_number = request.POST['account_number']
                account_period = request.POST['account_period']
                return HttpResponseRedirect('/tuples/budget1_go/'+account_number+'/'+account_period+'/'+p_d_o+'/')
#                for x in range(1,13):
#                    if accounting_period.objects.filter(month=x,year=account_period).count() == 0:
#                        accounting_period.objects.create(month=x,year=account_period)
#                    else:
#                        pass
#                acc_period = accounting_period.objects.filter(year=account_period)
#                acc = Account.objects.get(account_number=account_number)
#                year = " "+account_period[-2:]
#                account_object = Account.objects.get(account_number=account_number)
#                for y in acc_period:
#                    if Budget1.objects.filter(accounting_period=y,account=account_object).count() == 0:
#                        Budget1.objects.create(accounting_period=y,amount=0,account=account_object)
#                    else:
#                        pass
#                level = account_object.account_level
#                if level == "High" and account_object.account_number in parent_acc_list:
#                    medium_accounts = Account.objects.filter(parent_account=account_number)
#                    for acc in medium_accounts:
#                        for y in acc_period:
#                            if Budget1.objects.filter(accounting_period=y,account=acc).count() == 0:
#                                Budget1.objects.create(accounting_period=y,amount=0,account=acc)
#                            else:
#                                pass
#                    low_accounts = Account.objects.filter(account_level="Low")
#                    for acc in low_accounts:
#                        for y in acc_period:
#                            if Budget1.objects.filter(accounting_period=y,account=acc).count() == 0:
#                                Budget1.objects.create(accounting_period=y,amount=0,account=acc)
#                            else:
#                                pass
#                    
#                    budget = Budget1.objects.filter(accounting_period__year__contains=int(account_period))
#                    return render_to_response('budget1.html',{'current_year':current_year,'current_month':current_month,'z':int(account_period),'acc_period':acc_period,'budget':budget,'year_f':int(account_period),'low_accounts':low_accounts,'medium_accounts':medium_accounts,'mm':account_object.account_number,'selected_account':account_object,'year':year,'account':account},RequestContext(request))
            else:
                if p_d_o == "2":
                    account_number = request.POST['account_number']
                    account_period = request.POST['account_period']
                    return HttpResponseRedirect('/tuples/budget1_go/'+account_number+'/'+account_period+'/'+p_d_o+'/')
#                    current_month = date.today().month
#                    current_year = date.today().year
#                    year = " "+account_period[-2:]
#                    for x in range(1,13):
#                        if accounting_period.objects.filter(month=x,year=account_period).count() == 0:
#                            accounting_period.objects.create(month=x,year=account_period)
#                        else:
#                            pass
#                    acc_period = accounting_period.objects.filter(year=account_period)
#                    account_object = Account.objects.get(account_number=account_number)
#                    year = " "+account_period[-2:]
#                    level = account_object.account_level
#                    if level == "High" and account_object.account_number in parent_acc_list:
#                        for y in acc_period:
#                            if Budget1.objects.filter(accounting_period=y,account=account_object).count() == 0:
#                                Budget1.objects.create(accounting_period=y,amount=0,account=account_object)
#                            else:
#                                pass
#                        medium_accounts = Account.objects.filter(parent_account=account_number)
#                        for acc in medium_accounts:
#                            for y in acc_period:
#                                if Budget1.objects.filter(accounting_period=y,account=acc).count() == 0:
#                                    Budget1.objects.create(accounting_period=y,amount=0,account=acc)
#                                else:
#                                    pass
#                        low_accounts = Account.objects.filter(account_level="Low")
#                        for acc in low_accounts:
#                            for y in acc_period:
#                                if Budget1.objects.filter(accounting_period=y,account=acc).count() == 0:
#                                    Budget1.objects.create(accounting_period=y,amount=0,account=acc)
#                                else:
#                                    pass
#                    list_low_parent_acc = []
#                    sub_accounts = Sub_Accountt.objects.all()
#                    for sub_acc in sub_accounts:
#                        list_low_parent_acc.append(sub_acc.parent_account_number)
#                    budget = Budget1.objects.filter(accounting_period__year__contains=int(account_period))
#                    actuals = Actual.objects.filter(accounting_period__year__contains=int(account_period))
#                    print budget
#                    return render_to_response('budget1_actual.html',{'list_low_parent_acc':list_low_parent_acc,'low_accounts':low_accounts,'dict':dict,'current_month':current_month,'actuals':actuals,'budget':budget,'medium_accounts':medium_accounts,'year':year,'year_f':int(account_period),'selected_account':account_object},RequestContext(request))
#                
                    
    else:
        return render_to_response('budget1.html',{'account':account},RequestContext(request))
    
def budget1_go(request,account_number,account_period,p_d_o):
    list_low_parent_acc = []
    sub_accounts = Sub_Accountt.objects.all()
    acc_period = accounting_period.objects.filter(year=account_period)
    
    for sub_acc in sub_accounts:
        list_low_parent_acc.append(sub_acc.parent_account_number)
    if request.method=='POST':
        if 'go' in request.POST:
            account_number = request.POST['account_number']
            account_period = request.POST['account_period']
            p_d_o = request.POST['p_d_o']
            return HttpResponseRedirect('/tuples/budget1_go/'+account_number+'/'+account_period+'/'+p_d_o+'/')
        if 'save' in request.POST:
            account_object = Account.objects.get(account_number=account_number)
            medium_accounts = Account.objects.filter(parent_account=account_number)
            low_accounts = Account.objects.filter(Q(account_level="Low")&Q(parent_account__in=Account.objects.filter(parent_account=account_number).values_list('account_number')))
            g = Budget1.objects.filter(Q(accounting_period__in=acc_period)&(Q(account__in=medium_accounts)|Q(account__in=low_accounts)|Q(account=account_object)))
            acc_list=Account.objects.filter(account_level=str("Medium"),parent_account=request.POST['account_number'])
            for bud in g:
                try:
                    amount = request.POST[str(bud.id)]
                    Budget1.objects.filter(id=bud.id).update(amount=amount)
#                    for acc in acc_list:
#                        acc_low = Account.objects.filter(parent_account=acc.account_number)
#                        i=0
#                        for acc_l in acc_low:
#                            budget_amount = Budget1.objects.get(account=acc_l,accounting_period=bud.accounting_period)
#                            i=i+budget_amount.amount
#                        Budget1.objects.filter(account=acc,accounting_period=bud.accounting_period).update(amount=i)
#                    acc = Account.objects.get(account_number=request.POST['account_number'])
#                    acc_med = Account.objects.filter(parent_account=request.POST['account_number']) 
#                    i=0
#                    for acc_m in acc_med:
#                        budget_amount = Budget1.objects.get(account=acc_m,accounting_period=bud.accounting_period)
#                        i=i+budget_amount.amount
#                    Budget1.objects.filter(account=acc,accounting_period=bud.accounting_period).update(amount=i)
                except:
                    pass
            year = " "+account_period[-2:]
            account_object = Account.objects.get(account_number=account_number)
            budget = Budget1.objects.filter(Q(accounting_period__in=acc_period)&(Q(account__in=medium_accounts)|Q(account__in=low_accounts)|Q(account=account_object)))
            list_low_parent_acc = []
            sub_accounts = Sub_Accountt.objects.all()
            for sub_acc in sub_accounts:
                list_low_parent_acc.append(sub_acc.parent_account_number)
            actuals = Actual.objects.filter(accounting_period__year__contains=account_period)
            if p_d_o == "2":
                return render_to_response('budget1_actual.html',{'current_year':date.today().year,'list_low_parent_acc':list_low_parent_acc,'low_accounts':low_accounts,'medium_accounts':medium_accounts,'range':range(1,13),'list_low_parent_acc':list_low_parent_acc,'current_month':date.today().month,'actuals':actuals,'budget':budget,'year':year,'year_f':int(account_period),'selected_account':account_object},RequestContext(request))
            if p_d_o == "1":
                return render_to_response('budget1.html',{'list_low_parent_acc':list_low_parent_acc,'range':range(1,13),'current_year':date.today().year,'current_month':date.today().month,'z':int(account_period),'acc_period':account_period,'budget':budget,'year_f':int(account_period),'low_accounts':low_accounts,'medium_accounts':medium_accounts,'mm':account_object.account_number,'selected_account':account_object,'year':year,'account':account},RequestContext(request))
    if p_d_o == "2":
        current_month = date.today().month
        current_year = date.today().year
        year = " "+account_period[-2:]
        for x in range(1,13):
            if accounting_period.objects.filter(month=x,year=account_period).count() == 0:
                accounting_period.objects.create(month=x,year=account_period)
            else:
                pass
        acc_period = accounting_period.objects.filter(year=account_period)
        account_object = Account.objects.get(account_number=account_number)
        year = " "+account_period[-2:]
        level = account_object.account_level
        if level == "High" :
            for y in acc_period:
                if Budget1.objects.filter(accounting_period=y,account=account_object).count() == 0:
                    Budget1.objects.create(accounting_period=y,amount=0,account=account_object)
                else:
                    pass
            medium_accounts = Account.objects.filter(parent_account=account_number)
            for acc in medium_accounts:
                for y in acc_period:
                    if Budget1.objects.filter(accounting_period=y,account=acc).count() == 0:
                        Budget1.objects.create(accounting_period=y,amount=0,account=acc)
                    else:
                        pass
            low_accounts = Account.objects.filter(account_level="Low")
            for acc in low_accounts:
                for y in acc_period:
                    if Budget1.objects.filter(accounting_period=y,account=acc).count() == 0:
                        Budget1.objects.create(accounting_period=y,amount=0,account=acc)
                    else:
                        pass
        budget = Budget1.objects.filter(Q(accounting_period__in=acc_period)&(Q(account__in=medium_accounts)|Q(account__in=low_accounts)|Q(account=account_object)))
        actuals = Actual.objects.filter(accounting_period__in=acc_period)
        return render_to_response('budget1_actual.html',{'current_year':date.today().year,'range':range(1,13),'list_low_parent_acc':list_low_parent_acc,'low_accounts':low_accounts,'current_month':current_month,'actuals':actuals,'budget':budget,'medium_accounts':medium_accounts,'year':year,'year_f':int(account_period),'selected_account':account_object},RequestContext(request))
    
    if p_d_o == '1':
        for x in range(1,13):
            if accounting_period.objects.filter(month=x,year=account_period).count() == 0:
                accounting_period.objects.create(month=x,year=account_period)
            else:
                pass
        acc_period = accounting_period.objects.filter(year=account_period)
        year = " "+account_period[-2:]
        account_object = Account.objects.get(account_number=account_number)
        for y in acc_period:
            if Budget1.objects.filter(accounting_period=y,account=account_object).count() == 0:
                Budget1.objecyearts.create(accounting_period=y,amount=0,account=account_object)
            else:
                pass
        level = account_object.account_level
        if level == "High":
            medium_accounts = Account.objects.filter(parent_account=account_number)
            for acc in medium_accounts:
                for y in acc_period:
                    if Budget1.objects.filter(accounting_period=y,account=acc).count() == 0:
                        Budget1.objects.create(accounting_period=y,amount=0,account=acc)
                    else:
                        pass
            low_accounts = Account.objects.filter(account_level="Low")
            for acc in low_accounts:
                for y in acc_period:
                    if Budget1.objects.filter(accounting_period=y,account=acc).count() == 0:
                        Budget1.objects.create(accounting_period=y,amount=0,account=acc)
                    else:
                        pass
            budget = Budget1.objects.filter(accounting_period__year__contains=int(account_period))
            return render_to_response('budget1.html',{'list_low_parent_acc':list_low_parent_acc,'range':range(1,13),'current_year':date.today().year,'current_month':date.today().month,'z':int(account_period),'acc_period':acc_period,'budget':budget,'year_f':int(account_period),'low_accounts':low_accounts,'medium_accounts':medium_accounts,'mm':account_object.account_number,'selected_account':account_object,'year':year,'account':account},RequestContext(request))
    
def budget1_actual_low_acc(request,acc_no,year):
    sub_accounts = Sub_Accountt.objects.filter(parent_account_number=acc_no)
    current_month = date.today().month
    actuals = Actual.objects.filter(accounting_period__year__contains=year)
    acc_period = accounting_period.objects.filter(year=year)
    for acc in sub_accounts:
        for t_p in acc_period:
            if Budget1.objects.filter(sub_account=acc,accounting_period=t_p).count() ==0:
                Budget1.objects.create(sub_account=acc,accounting_period=t_p,amount=0)
            else:
                pass
    budget = Budget1.objects.filter(accounting_period__in=acc_period,sub_account__in=sub_accounts)
    if request.method=="POST":
        for bud in budget:
            try:
                amount = request.POST[str(bud.id)]
                Budget1.objects.filter(id=bud.id).update(amount=amount)
            except Exception,e:
                pass
        for t_p in acc_period:
            low_acc = Account.objects.get(account_number=acc_no)
            i=0
            for sub_acc in Sub_Accountt.objects.filter(parent_account_number=low_acc.account_number):
                amount = Budget1.objects.get(accounting_period=t_p,sub_account=sub_acc).amount
                i=i+amount
            Budget1.objects.filter(account=low_acc,accounting_period=t_p).update(amount=i)
            med_acc = Account.objects.get(account_number=low_acc.parent_account)
            j=0
            for low_acc in Account.objects.filter(parent_account=med_acc.account_number):
                amount = Budget1.objects.get(accounting_period=t_p,account=low_acc).amount
                j=j+amount
            Budget1.objects.filter(accounting_period=t_p,account=med_acc).update(amount=j)
            high_acc = Account.objects.get(account_number=med_acc.parent_account)
            k=0
            for med_acc in Account.objects.filter(parent_account= high_acc.account_number):
                amount = Budget1.objects.get(account=med_acc,accounting_period=t_p).amount
                k=k+amount
            Budget1.objects.filter(accounting_period=t_p,account=high_acc).update(amount=k)
        budget = Budget1.objects.filter(accounting_period__year__contains=year)
        return render_to_response('budget1_actual_low_acc.html',{'win_close':'1'},RequestContext(request))
    else:
        year = " "+year[-2:]
        return render_to_response('budget1_actual_low_acc.html',{'current_year':date.today().year,'year':year,'range':range(1,13),'current_month':current_month,'actuals':actuals,'budget':budget,'sub_acc':sub_accounts},RequestContext(request))

def budget1_budget_low_acc(request,acc_no,year):
    sub_accounts = Sub_Accountt.objects.filter(parent_account_number=acc_no)
    current_month = date.today().month
    acc_period = accounting_period.objects.filter(year=year)
    for acc in sub_accounts:
        for t_p in acc_period:
            if Budget1.objects.filter(sub_account=acc,accounting_period=t_p).count() ==0:
                Budget1.objects.create(sub_account=acc,accounting_period=t_p,amount=0)
            else:
                pass
    budget = Budget1.objects.filter(accounting_period__in=acc_period)
    if request.method=="POST":
        for bud in budget:
            try:
                amount = request.POST[str(bud.id)]
                Budget1.objects.filter(id=bud.id).update(amount=amount)
            except Exception,e:
                pass
        for t_p in acc_period:
            low_acc = Account.objects.get(account_number=acc_no)
            i=0
            for sub_acc in Sub_Accountt.objects.filter(parent_account_number=low_acc.account_number):
                amount = Budget1.objects.get(accounting_period=t_p,sub_account=sub_acc).amount
                i=i+amount
            Budget1.objects.filter(account=low_acc,accounting_period=t_p).update(amount=i)
            med_acc = Account.objects.get(account_number=low_acc.parent_account)
            j=0
            for low_acc in Account.objects.filter(parent_account=med_acc.account_number):
                amount = Budget1.objects.get(accounting_period=t_p,account=low_acc).amount
                j=j+amount
            Budget1.objects.filter(accounting_period=t_p,account=med_acc).update(amount=j)
            high_acc = Account.objects.get(account_number=med_acc.parent_account)
            k=0
            for med_acc in Account.objects.filter(parent_account= high_acc.account_number):
                amount = Budget1.objects.get(account=med_acc,accounting_period=t_p).amount
                k=k+amount
            Budget1.objects.filter(accounting_period=t_p,account=high_acc).update(amount=k)
        budget = Budget1.objects.filter(accounting_period__year__contains=year)
        return render_to_response('budget1_budget_low_acc.html',{'win_close':'1'},RequestContext(request))
    else:
        year = " "+year[-2:]
        return render_to_response('budget1_budget_low_acc.html',{'current_year':date.today().year,'year':year,'range':range(1,13),'current_month':current_month,'budget':budget,'sub_acc':sub_accounts},RequestContext(request))
    