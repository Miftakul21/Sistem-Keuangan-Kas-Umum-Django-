from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, AddUserForm, UpdateUserForm, AddBook
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from base.models import User, Buku
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else: 
                print('invalid credentials')
                # message = 'invalid credentials'
        else: 
            print('error validation form')
            # message = 'error validation form'
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Anda berhasil logout')
    return redirect('login')

@login_required
def dashboard_view(request):
    if request.user.is_authenticated:
        buku = Buku.objects.filter(deleted_at__isnull=False)

        # Soft Delete
        for item in buku:
            item.deleted_at = time_ago_in_word(item.deleted_at)

        items = Buku.objects.filter(deleted_at__isnull=True)
        jumlah_item = 0
        saldo = 0
        debet = 0
        jumlah_saldo = 0

        for item in items:
            jumlah_item += 1 # jumlah item
            if item.saldo: 
                jumlah_saldo += item.saldo
                saldo += item.saldo # jumlah saldo
            elif item.debet:
                jumlah_saldo -= item.debet
                debet += item.debet # jumlah debet

        return render(request, 'dashboard.html', {'buku': buku, 'item': jumlah_item, 'saldo': saldo, 'debet': debet , 'jumlah_saldo': jumlah_saldo })
    return redirect('login')

@login_required
def user_view(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        return render(request, 'user.html', {'users': users})
    
    return redirect('login')

@login_required
def add_user_view(request):
    form = AddUserForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.instance.password = make_password(request.POST.get('password'))
                form.save()
                messages.success(request, 'Successfully add record')
                return redirect('user')

        return render(request, 'add_user.html', {'form': form})
    return redirect('login')

@login_required
def edit_user_view(request, pk):
    if request.user.is_authenticated:
        current_record = User.objects.get(id=pk)
        form = UpdateUserForm(request.POST or None, instance=current_record)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated record')
            return redirect('user')
        
        return render(request, 'edit_user.html', {'form': form})
    
    return redirect('login')

@login_required
def delete_user_view(request, pk):
    if request.user.is_authenticated:
        User.objects.get(id=pk).delete()
        messages.success(request, 'Successfully delete user')
        return redirect('user')

    return redirect('login')

@login_required
def buku_view(request):
    if request.user.is_authenticated:
        buku_kas = Buku.objects.filter(deleted_at__isnull=True)
        return render(request, 'buku.html', {'buku_kas': buku_kas})

    return redirect('login')

@login_required
def add_buku_view(request):
    if request.user.is_authenticated:
        form = AddBook(request.POST or None)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('buku')
        
        return render(request, 'add_buku.html', {'form': form})
        
    return redirect('login')

@login_required
def edit_buku_view(request, pk):
    if request.user.is_authenticated:
        current_record = Buku.objects.get(id=pk)
        form = AddBook(request.POST or None, instance=current_record)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Successfully update buku')
            return redirect('buku')
        
        return render(request, 'edit_buku.html', {'form': form})

    return redirect('login')

@login_required
def delete_buku_view(request, pk):
    if request.user.is_authenticated:
        buku_kas = Buku.objects.get(id=pk)
        buku_kas.user = request.user
        buku_kas.save()
        buku_kas.soft_delete()

        messages.success(request, 'Successfylly deleted buku')
        return redirect('buku')
    
    return redirect('login')

@login_required
def laporan_harian_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            tanggal = request.POST.get('tanggal')
            buku = data_kas_keuangan(tanggal, None)
            return render(request, 'laporan_harian.html', {'buku': buku })

        buku = data_kas_keuangan(None, None)       
        return render(request, 'laporan_harian.html', {'buku': buku })
    
    return redirect('login')
        
@login_required
def laporan_bulanan_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            tanggal_awal = request.POST.get('tanggal_awal')
            tanggal_akhir = request.POST.get('tanggal_akhir')
            buku = data_kas_keuangan(tanggal_awal, tanggal_akhir)

            return render(request, 'laporan_bulanan.html', {'buku': buku, })

        buku = data_kas_keuangan(None,None)
        return render(request, 'laporan_bulanan.html', {'buku': buku, })
    
    return redirect('login')

def data_kas_keuangan(tanggal_awal, tanggal_akhir):
    buku = ''
    if tanggal_awal is None and tanggal_akhir is None:
        buku = Buku.objects.filter(deleted_at__isnull=True)

    if tanggal_awal is not None and tanggal_akhir is not None:
        buku = Buku.objects.filter(deleted_at__isnull=True).filter(tanggal__range=[tanggal_awal, tanggal_akhir])

    elif tanggal_awal is not None and tanggal_akhir is None:
        buku = Buku.objects.filter(deleted_at__isnull=True).filter(tanggal=tanggal_awal)

    data = []
    total = 0
    total_saldo = 0
    total_debet = 0

    for datas in buku:
        if datas.saldo:
            total += datas.saldo
            total_saldo += datas.saldo
        elif datas.debet:
            total -= datas.debet
            total_debet = datas.debet

        data.append({
            'tanggal': datas.tanggal,
            'keterangan_kas': datas.keterangan_kas,
            'saldo': datas.saldo,
            'debet': datas.debet,
            'total': total
        })

    return {'data': data, 'total_saldo': total_saldo, 'total_debet': total_debet}
    

def time_ago_in_word(date):
    delta = timezone.now() - date

    if delta.total_seconds() < 60:
        return 'beberapa detik yang lalu'
    elif delta.total_seconds() < 3600:
        return f'{int(delta.total_seconds() / 60)} menit yang lalu'
    elif delta.total_seconds() < 86400:
        return f'{int(delta.total_seconds() / 3600)} jam yang lalu'
    elif delta.days < 7:
        return f'{delta.days} hari yang lalu'
    else:
        return f'{delta.days // 7} minggu yang lalu'