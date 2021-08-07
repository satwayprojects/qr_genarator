from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from .forms import *
from .models import *
import os
from django.contrib.auth import authenticate, logout, login

# for generating the QR code
from reportlab_qrcode import QRCodeImage
# for excel writing
import xlwt
from django.contrib.auth.decorators import login_required
# Create your views here.

# function for generating the initial QR
@login_required
def qr_generatefun(request):
    # fetching the count from the table QRgenerate
    batchA = QRgenerate.objects.filter(batch='A').count()
    batchB = QRgenerate.objects.all().filter(batch='B').count()
    batchC = QRgenerate.objects.all().filter(batch='C').count()
    total = QRgenerate.objects.all().count()
    number = total+1

    if request.method == 'GET':
    # fetching the last entered UIN  
        try:
            last_uin = QRgenerate.objects.latest('uin')
            print(last_uin.uin)
            return render(request,'qr_generate.html',{'number':number,'data':last_uin,'countA':batchA,'countB':batchB,'countC':batchC,'total':total})
        except:
            return render(request,'qr_generate.html',{'number':number,'countA':batchA,'countB':batchB,'countC':batchC,'total':total})
    else:
        vyom = request.POST['vyom']
        year = request.POST.get('year')
        month = request.POST.get('month')
        batch = request.POST.get('batch')
        device_start= int(request.POST.get('deviceStart'))
        count=int(request.POST.get('count'))
        uin = vyom+year+month+batch
        # Name to the PDF
        pdf_name = year+month+batch+str(device_start)+"end"+str(device_start+count-1)+ ".pdf"
        # Path to the PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % pdf_name
        # save_name = os.path.join(os.path.expanduser("~"), "Desktop/UIN", pdf_name)
        # PDF creation
        doc = Canvas(response,pagesize=(38 * mm, 12*mm))
        print(uin)
        for i in range(count):
            # Function for drawing the QR and saving the UIN, Serialno and Batch
            def qr_generate(UIN,B,C):

                qrgen = QRgenerate.objects.create(batch=B,uin=UIN ,count=C)
                qrgen.save()
                qr = QRCodeImage(UIN, size= 10 * mm)
                qr.drawOn(doc, 0,3)
                doc.setFont("Times-Roman", 7.5)
                doc.drawString(26, 13, UIN)
                doc.showPage()
            series_no = device_start + i
            series_no = str(series_no)
            if len(series_no) > 5:
                context = {'error_message': 'Series number is allowed to 99999','number':number,'countA':batchA,'countB':batchB,'countC':batchC,'total':total}
                return render(request,'qr_generate.html',context) 
            else:    
                UIN= uin+series_no.zfill(5)
                try:
                    qr_generate(UIN,batch,series_no.zfill(5))
                except:
                    context = {'error_message': 'UIN already exists','number':number,'countA':batchA,'countB':batchB,'countC':batchC,'total':total}
                    return render(request,'qr_generate.html',context)     
        doc.save()
        return response  
        
        
        # last_uin = QRgenerate.objects.latest()
        # batchA = QRgenerate.objects.filter(batch='A').count()
        # batchB = QRgenerate.objects.all().filter(batch='B').count()
        # batchC = QRgenerate.objects.all().filter(batch='C').count()
        # total = QRgenerate.objects.all().count()
        # number = total+1
        # context = {'success_message': 'UIN generated successfully','number':number,'data':last_uin,'countA':batchA,'countB':batchB,'countC':batchC,'total':total}
        # return render(request,'qr_generate.html',context)

# Linking the UIN with ICCID AND IMEI 
@login_required         
def uin_linkfun(request):
    currentuser=request.user 
    print(currentuser)   
    if request.method == 'POST':
        nuf = NewUinLinkForm(request.POST)  
        if nuf.is_valid():
            uin_table=UinLinK()
            uin_table.imei= request.POST.get('imei')
            uin_table.iccid= request.POST.get('iccid')
            uin_table.uin_id= request.POST.get('uin')
            user=str(currentuser)
            uin_table.added_by=user
            uin_table.save()

            # nuf.save()
            nuf = NewUinLinkForm()
            
            context = {'success_message': 'Device details added successfully','data':nuf}
            return render(request,'uin_link.html',context)  
        else:
            context = {'error_message': 'Please enter valid data','data':nuf} 
            return render(request,'uin_link.html',context)      
    else:
        nuf = NewUinLinkForm()
        return render(request,'uin_link.html',{'data':nuf})

# Final QR generating for IMEI
@login_required
def imei_generatefun(request):
    if request.method == 'POST':
        UIN = request.POST['uin']
        try:
            uin_exist = UinLinK.objects.get(uin = UIN)
            uin = uin_exist.uin_id
            # print(uin)
            imei = uin_exist.imei
            # print(imei)
            iccid = uin_exist.iccid
            # print(iccid)
            pdf_name = uin + ".pdf"
            # print(pdf_name)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="%s"' % pdf_name
            # save_name = os.path.join(os.path.expanduser("~"), "Desktop/IMEI", pdf_name)
            doc = Canvas(response,pagesize=(60 * mm, 20*mm))
            for i in range(2):
                qr = QRCodeImage(imei, size= 18 * mm)
                qr.drawOn(doc, -3,3.5)
                doc.setFont("Helvetica-Bold", 8.5)
                doc.drawString(44,40,"IMEI")
                doc.drawString(67, 40,":"+imei)
                doc.drawString(44,25,"UIN")
                doc.drawString(67, 25, ":"+uin)                
                doc.drawString(44,10,"CCID")
                doc.drawString(67, 10, ":"+iccid)
                doc.showPage()
                i = i+1
            doc.save()
            return response
            # return render(request,'imei_generate.html',{'data':uin_exist,'success_message': 'IMEI generated Successfully'})
        except:
            context = {'error_message': 'UIN does not exists'}
            return render(request,'imei_generate.html',context)

    else:
        return render(request,'imei_generate.html')
#   Function for getting the count of final products
@login_required
def productfun(request):
    if request.method =='GET':
        # Accessing the two tables using select_related
        batchA = UinLinK.objects.all().select_related('uin').filter(uin__batch='A').count()
        batchB = UinLinK.objects.all().select_related('uin').filter(uin__batch='B').count()
        batchC = UinLinK.objects.all().select_related('uin').filter(uin__batch='C').count()
        total = UinLinK.objects.all().select_related('uin').count()
        return render(request,'product.html',{'countA':batchA,'countB':batchB,'countC':batchC,'total':total})

# downloading the excel sheets 
@login_required
def export_excelfun(request):
    if request.method =='GET':
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="VYOM.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Device Data') # this will make a sheet named Users Data

    # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['DATE','UIN', 'IMEI', 'ICCID', 'BATCH']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = UinLinK.objects.all().select_related('uin').values_list('date','uin','imei','iccid', 'uin__batch')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
                print(row[col_num])

        wb.save(response)
    
        return response

def loginfun(request):
    if request.method=='POST':
        usern= request.POST.get('username')
        pswd= request.POST.get('password')
        try:
            user= authenticate(request,username=usern,password=pswd)

            if user is not None and user.is_superuser == 1 and user.is_staff==1:
                login(request,user)
                return redirect('QRgenerate/')
            else:
                login(request,user) 
                return redirect('UINlink/')
        except:
            context = {'error_message': ' Incorrect Credentials'}
            return render (request,'login.html',context)

    else:
        return render (request,'login.html')
def logoutfun(request):
    logout(request)
    return redirect('/')
@login_required
def adminfun(request):
    currentuser=request.user 
    if currentuser is not None and currentuser.is_superuser == 1 and currentuser.is_staff==1:
        if request.method=="GET":
            return render(request,'admin.html')
        else:
            uin= request.POST.get('uin')
            try:
                data = UinLinK.objects.get(uin=uin)
                return render(request,'admin.html',{'data': data})
                
            except:
                context = {'error_message': ' UIN does not exist'}
                return render(request,'admin.html',context)
    else:
        return redirect('/QRgenerate/')
@login_required
def registerfun(request):
    currentuser=request.user 
    if currentuser is not None and currentuser.is_superuser == 1 and currentuser.is_staff==1:
        if request.method =='POST':
            form = NewUserForm(request.POST)
            if form.is_valid():
                name = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
                User.objects.create_user(username=name,
                                     first_name=name,
                                     email=email,
                                     password=password,
                                     is_staff=1,
                                     is_superuser=0
                                    )
                form= NewUserForm()
                context = {'form':form,'success_message': 'Registration Successful.'}             
                return render(request,'registration.html',context)
            else:
            
            # context = {"status":"",'form':form} 
                context = {'form':form,'error_message': 'Registration Failed.'}   
                return render(request,'registration.html',context)
        else:
            form= NewUserForm()
            context = {"status":"",'form':form}  
            return render(request,'registration.html',context)
    else:
        return redirect('/QRgenerate/')

@login_required
def staff_fun(request):
    currentuser=request.user 
    if currentuser is not None and currentuser.is_superuser == 1 and currentuser.is_staff==1:
        usr = User.objects.filter(is_superuser = 0, is_staff=1)
        return render(request,'staff.html',{'data':usr})
    else:
        return redirect('/QRgenerate/')


@login_required
def staff_deletefun(request,id):
    currentuser=request.user 
    if currentuser is not None and currentuser.is_superuser == 1 and currentuser.is_staff==1:

        staff_del= User.objects.get(id=id)
        staff_del.delete()
        return redirect('/staff/')
    else:
        return redirect('/QRgenerate/')

def duplicate_generatefun(request):
    if request.method=="POST":
        uin= request.POST.get('d_uin')
        try:
            uin_exist = QRgenerate.objects.get(uin = uin)
            uinpdf=uin+".pdf"
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="%s"' %uinpdf
            # save_name = os.path.join(os.path.expanduser("~"), "Desktop/UIN", uin+".pdf")
            doc = Canvas(response,pagesize=(38 * mm, 12*mm))
            qr = QRCodeImage(uin, size= 10 * mm)
            qr.drawOn(doc, 0,3)
            doc.setFont("Times-Roman", 7.5)
            doc.drawString(26, 13, uin)
            doc.showPage()
            doc.save()
            return response
        except:
            return redirect('/QRgenerate/')
    else:
        return redirect('/QRgenerate/')



        

