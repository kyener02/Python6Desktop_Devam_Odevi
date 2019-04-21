import sys
import os
from AnaDB import Veritabani
from PyQt5.QtWidgets import QApplication,QMainWindow,QTableWidgetItem,QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from dialog import Dialog
class Ana(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        ## veritabanı ve arayüz dosyaları çağırılıyor
        self.vt = Veritabani(os.getcwd()+r"\IEDB.db")
        self.win = uic.loadUi(os.getcwd()+r"\ana.ui")
        self.secilenAy = "Seçiniz"
        self.secilenKalem = "Seçiniz"
        ## Arayüzdeki nesneler veritabanından dolduruluyor
        self.InitUI()
        self.TabloDoldur()
        ## Arayüzdeki Nesnelere Fonksiyonlar Atanıyor
        self.win.btYeni.clicked.connect(self.InitUI)
        self.win.lstHarcama.itemDoubleClicked.connect(self.secim)
        self.win.btKaydet.clicked.connect(self.Kaydet)
        self.win.btSil.clicked.connect(self.Sil)
        self.win.cmbAy.currentTextChanged.connect(self.SecimAy)
        self.win.cmbKalem.currentTextChanged.connect(self.SecimKalem)
        #Menü ile ilişkilendirme
        self.win.action_k.triggered.connect(self.win.close)
        self.win.actionKaydet.triggered.connect(self.Kaydet)
        self.win.actionG_ncelle.triggered.connect(self.Kaydet)
        self.win.actionSil.triggered.connect(self.Sil)
        self.win.actionTemizle.triggered.connect(self.InitUI)
        self.win.actionKalem_Ekle.triggered.connect(self.PencereAc)
        self.dialog = Dialog(self) 
        ## Ekranda Gösterim için
        self.win.show()



    def PencereAc(self):
        self.dialog.pencere.show()
         

    def SecimAy(self,deger):
        self.secilenAy = deger
        self.TabloDoldur()
    def SecimKalem(self,deger):
        self.secilenKalem = deger
        self.TabloDoldur()


    def Sil(self):
        ID = self.win.lblKayit.text()
        if self.Mesaj(4,"Silme İşlemi","Silmek İstediğinizden Emin Misiniz?"):
            sonuc = self.vt.VeriSil(ID)
            if sonuc == "1":
                self.Mesaj(1,"Silme İşlemi","Silme Gerçekleşti")
                self.InitUI()
                self.TabloDoldur()
            else:
                self.Mesaj(2,"Silme İşlemi",sonuc)



    def secim(self):
        # print(self.liste[self.win.lstHarcama.currentRow()])
        tutar = str(self.liste[self.win.lstHarcama.currentRow()][2])
        ID = str(self.liste[self.win.lstHarcama.currentRow()][0])
        self.win.lblKayit.setText(ID)
        self.win.txtTutar.setText(tutar)
        self.win.cmbKalem.setCurrentText(self.liste[self.win.lstHarcama.currentRow()][1])
        self.win.cmbAy.setCurrentText(self.liste[self.win.lstHarcama.currentRow()][3])   

    def Mesaj(self,icon,baslik,metin):
        sonuc = True
        if icon == 1:
            QMessageBox.information(self,baslik,metin,QMessageBox.Ok)
        elif icon == 2:
            QMessageBox.critical(self,baslik,metin,QMessageBox.Ok)
        elif icon == 3:
            QMessageBox.warning(self,baslik,metin,QMessageBox.Ok)
        elif icon == 4:
            try:
                cevap =  QMessageBox.question(self,baslik,metin,QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Cancel)
                if cevap == QMessageBox.Ok:
                    sonuc = True
                else:
                    sonuc = False
            except:
                print("Hata")
        return sonuc


    def Kaydet(self):
        ID = self.win.lblKayit.text()
        kalem = self.win.cmbKalem.currentIndex()
        ay = self.win.cmbAy.currentIndex()
        tutar =  self.win.txtTutar.text()
        if ID == "":
            sonuc = self.vt.VeriEkle(kalem,ay,tutar)
        else:
            sonuc = self.vt.VeriGuncelle(kalem,ay,tutar,ID)
        
        if sonuc == "1":
            self.Mesaj(1,"Bilgi","Başarıyla Kaydedildi")
            self.InitUI()
            self.TabloDoldur()
        else:
            self.Mesaj(2,"Kayıt Hatası",sonuc)
    def TabloDoldur(self):
        self.win.lstHarcama.clear()
        self.liste = self.vt.Listele(self.secilenAy,self.secilenKalem)
        self.win.lstHarcama.setHorizontalHeaderLabels(("ID","KALEM","TUTAR","AY"))
        self.win.lstHarcama.setRowCount(15)
        self.win.lstHarcama.setColumnCount(4)
        satir = 0
        for a,b,c,d in self.liste:
            self.win.lstHarcama.setItem(satir,0,QTableWidgetItem(str(a)))
            self.win.lstHarcama.setItem(satir,1,QTableWidgetItem(str(b)))
            self.win.lstHarcama.setItem(satir,2,QTableWidgetItem(str(c)))
            self.win.lstHarcama.setItem(satir,3,QTableWidgetItem(str(d)))
            satir += 1

        

    def InitUI(self):
        # Ay 
        self.cmbAyDoldur()
        # Kalem
        self.cmbKalemDoldur()
        #Tutar
        self.win.txtTutar.setText("")
        self.win.lblKayit.setText("")

    def cmbAyDoldur(self):
        # Ay Combosu Dolduruluyor 
        self.win.cmbAy.clear()
        self.win.cmbAy.addItem("Seçiniz",-1)
        for a,b in self.vt.SozlukListele(2):
            self.win.cmbAy.addItem(a,b)
    
    def cmbKalemDoldur(self):
        # Kalem Combosu Dolduruluyor 
        self.win.cmbKalem.clear()
        self.win.cmbKalem.addItem("Seçiniz",-1)
        for a,b in self.vt.SozlukListele(1):
            self.win.cmbKalem.addItem(a,b)

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ana()
    sys.exit(app.exec_())




