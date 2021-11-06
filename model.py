# from enum import unique
# from operator import index
from peewee import *
# import configparser
import os
# import bcrypt
#get config path file
# config_path =os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir,"config.ini")

#read config
# config = configparser.ConfigParser()
# config.read(config_path)
# dbName = config['DATABASE']['DB_NAME']
dbName = "data.db"

# default_username = config['DEFAULT_ACCOUNT']['USERNAME']
# default_password = config['DEFAULT_ACCOUNT']['PASSWORD']
default_username = "admin"
default_password = "714c002346b3482e9fe4b42527c0d8d4a099a070066ca36cb9f15deeac3b66f0"
# passwd = b'admin@123'

# hashed = bcrypt.hashpw(passwd,bcrypt.gensalt())
# print(hashed)

#creat db file if it not exists
dbPath =os.path.join(os.path.dirname(os.path.abspath(__file__)),dbName)
db = SqliteDatabase(dbPath,pragmas={'foreign_keys': 1})
db.connect()

class BaseModel(Model):
    class Meta:
        database =db

#table user
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField(null=False)
    fullname = CharField(null=True)
    phoneNum = CharField(null=True,max_length=20)
    email = CharField(null=True)
    department = CharField(null=True,max_length=50)



#table Benh nhan
class Benhnhan(BaseModel):
    ho_ten = CharField(null=False,max_length=50)
    dia_chi = CharField(null=True )
    dien_thoai = CharField(default="",max_length=20)
    thoi_quen = TextField(null=True)
    benh_hay_mac = CharField(null=True)
    ghi_chu_BN = TextField(null=True)

    bac_si = CharField(null=True,max_length=50)
    benh_nen = CharField(null=True)
    di_ung = TextField(null=False)
    tien_su_benh = TextField(null=False)
    lich_su = TextField(null=True )
    phac_do = TextField(null=True )

    ma_bh = CharField(null=True,max_length=20 )
    nam_sinh = CharField(null=False,max_length=5 )
    gioi_tinh = CharField(null=True,max_length=10 )
    nghe_nghiep = CharField(null=True,max_length=30 )
    nhom_mau  = CharField(null=True,max_length=4 )
    benhan_tick = CharField(default="",max_length=1)
    noisoi_tick = CharField(default="",max_length=1)
    chuandoan_tick = CharField(default="",max_length=1)
    creat_at = TimestampField()
    # class Meta:
    #     indexes=(
    #         (('ho_ten','dia_chi','dien_thoai','thoi_quen','benh_hay_mac'),True)
    #     )

#table Benh an
class Benhan(BaseModel):
    can_nang = CharField(null=True,max_length=10)
    bac_si_chi = CharField(null=True,max_length=50 )
    tg_mac = CharField(null=True,max_length=50 )
    kham_lan = IntegerField(default=1 )
    li_do_kham = TextField(null=False )
    di_chuyen = CharField(null=True)
    ghi_chu = TextField(null=True )
    benhnhan = ForeignKeyField(Benhnhan,on_delete='CASCADE')
    creat_at = TimestampField()

class Noisoi(BaseModel):
    tc_cha = TextField(null = False )
    tc_con = TextField(null = False )
    chan_doan = TextField(null = False )
    mo_ta = TextField(null = False )
    image_url = TextField(null = False)
    benhan = ForeignKeyField(Benhan,on_delete='CASCADE')
    creat_at = TimestampField()
    sync_time = IntegerField(default=0)

#table chuan doan
class Chuandoan(BaseModel):
    danh_gia = TextField(null=True )
    chuan_doannt = TextField(null=True )
    ghi_chu = TextField(null=True)
    phac_do = TextField(null=True )
    don_thuoc = TextField(null=True )
    loi_dan = TextField(null=True )
    benhan = ForeignKeyField(Benhan,backref='chuandoans',on_delete='CASCADE')
    creat_at = TimestampField()

#table camera setting
class Camerasetting(BaseModel):
    device_id = IntegerField(null=False)
    small_size = CharField(null=False,max_length=10)
    light = IntegerField(null=False)

#table cai dat thiet bi
class Thietbi(BaseModel):
    ten = CharField(null=True )
    model = CharField(null=True )
    version = CharField(null=True)
    series_num = CharField(null=True )
    khach_hang = TextField(null=True )
    begin_date = CharField(null=True )
    update_date = CharField(null=True )
    cai_dat = TextField(null=True)

#table thong tin cloud
class Cloud(BaseModel):
    txt = CharField(null = True)
#table sync cloud
class Syncloud(BaseModel):
    status_operation = BooleanField(default=False)
    message = TextField(null = True)
    update_time =  TimestampField()
    interval_time = IntegerField(default=0) # chu ki dong bo

#table file sync cloud
class Filesync(BaseModel):
    imageUrl = TextField(null = False)
    update_time =  IntegerField(default=0)





############# cac table trong cai dat#######################

#table thong tin phong kham
class Phongkham(BaseModel):
    logo_url = TextField(null=False)
    ten_phong = CharField(null= False)
    dia_chi = CharField(null=False)
    dien_thoai = CharField(null = False)
    email =  CharField(null = False)

#table Mau in
class Mauin(BaseModel):
    mau_in = IntegerField(null=False)

#table Nghe nghiep
class Nghenghiep(BaseModel):
    nghe_nghiep = CharField(max_length=50,null=False)

#table Nghe nghiep
class Nhommau(BaseModel):
    mau = CharField(max_length=20,null=False)

#table thoigian mac
class Thoigian(BaseModel):
    thoi_gian_mac = TextField(null=False)

#table benh di truyen
class Benh(BaseModel):
    benh_di_truyen = CharField(null=False)

#table di ung
class Diung(BaseModel):
    di_ung = TextField(null=False)

#table li do kham
class Lido(BaseModel):
    li_do_kham = TextField(null=False)

#table tien su benh
class Tiensu(BaseModel):
    tien_su_benh = TextField(null=False)

#table to chuc cha
class Tcha(BaseModel):
    tc_cha = CharField(null=False,unique=True)

#table to chuc con
class Tcon(BaseModel):
    tc_con = CharField(null=False,unique=True)
    tc_cha = CharField(null=False)

#table danh gia
class Danhgia(BaseModel):
    danh_gia = TextField(null=False)

#table phac do
class Phacdo(BaseModel):
    phac_do = TextField(null=False)

#table loi dan
class Loidan(BaseModel):
    loi_dan = TextField(null=False)

#table chan doan
class Chandoan(BaseModel):
    chan_doan = TextField(null=False,unique=True)
    tc_con = CharField(null=False)
    tc_cha = CharField(null=False)

#table mo ta
class Mota(BaseModel):
    mo_ta = TextField(null=False,unique=True)
    tc_con = CharField(null=False)
    tc_cha = CharField(null=False)

#table danh muc thuoc
class Mucthuoc(BaseModel):
    ten_thuoc = TextField(null=False,unique=True)
    lieu_luong = CharField(null = False)
    cach_dung = TextField(null = False)




def creat_table():
    if db.table_exists(table_name='user')!=True:
        db.create_tables([User,Benhan,Benhnhan,Noisoi,Mauin,Phongkham,Nghenghiep,Nhommau,Thoigian,Benh,Diung,Lido,Tiensu,Tcha,Tcon,Danhgia,Phacdo,Loidan,Chandoan,Mota,Chuandoan,Camerasetting,Thietbi,Cloud,Syncloud,Mucthuoc,Filesync])
        User.create(username=default_username,password=default_password,fullname="NA")
        Mauin.create(mau_in = 0)
        Syncloud.create(message = 'init ',update_time =0,interval_time=100)
    # if db.table_exists(table_name='filesync')!=True:
    #     db.create_tables([Filesync])
        
def db_close():
    db.close()




