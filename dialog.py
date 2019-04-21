import sys
import os
from AnaDB import Veritabani
from PyQt5.QtWidgets import QApplication,QDialog,QTableWidgetItem,QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        ## veritabanı ve arayüz dosyaları çağırılıyor
        self.vt = Veritabani(os.getcwd()+r"\IEDB.db")
        self.pencere = uic.loadUi(os.getcwd()+r"\sozluk.ui")

        self.InitUI()
        self.TabloDoldur()

        self.pencere.btIptal.clicked.connect(self.pencere.close)
        self.pencere.lstSozluk.itemDoubleClicked.connect(self.Secim)
        self.pencere.btKaydet.clicked.connect(self.Kaydet)

    def InitUI(self):
        self.pencere.txtTablo.setText("")
        self.pencere.txtID.setText("")
        self.pencere.txtAd.setText("")

    def Secim(self):

        ID = str(self.liste[self.pencere.lstSozluk.currentRow()][0])
        sozluk_ID = str(self.liste[self.pencere.lstSozluk.currentRow()][1])
        sozluk_adi = str(self.liste[self.pencere.lstSozluk.currentRow()][2])
        tablo_ID = str(self.liste[self.pencere.lstSozluk.currentRow()][3])

        self.pencere.txtID.setText(sozluk_ID)
        self.pencere.txtAd.setText(sozluk_adi)
        self.pencere.txtTablo.setText(tablo_ID)
        self.pencere.lbl_ID.setText(ID)

    def TabloDoldur(self):
        self.pencere.lstSozluk.clear()
        self.liste = self.vt.DialogSozlukListele()
        self.pencere.lstSozluk.setHorizontalHeaderLabels(("ID", "SOZLUK ID","SOZLUK ADI","TABLO ID"))
        self.pencere.lstSozluk.setRowCount(15)
        self.pencere.lstSozluk.setColumnCount(4)
        satir = 0
        for a,b,c,d in self.liste:
            self.pencere.lstSozluk.setItem(satir, 0, QTableWidgetItem(str(a)))
            self.pencere.lstSozluk.setItem(satir, 1, QTableWidgetItem(str(b)))
            self.pencere.lstSozluk.setItem(satir, 2, QTableWidgetItem(str(c)))
            self.pencere.lstSozluk.setItem(satir, 3, QTableWidgetItem(str(d)))
            satir += 1

    def Kaydet(self):
        sozluk_ID = self.pencere.txtID.text()
        sozluk_adi = self.pencere.txtAd.text()
        tablo_ID = self.pencere.txtTablo.text() 
        ID = self.pencere.lbl_ID.text()
        
        if ID == "":
            sonuc = self.vt.DialogVeriEkle(sozluk_ID,sozluk_adi,tablo_ID)
        else:
            sonuc = self.vt.DialogVeriGuncelle(sozluk_ID,sozluk_adi,tablo_ID,ID)

        if sonuc == "1":
            self.Mesaj(1,"Bilgi","Başarıyla Kaydedildi")
            self.InitUI()
            self.TabloDoldur()
        else:
            self.Mesaj(2,"Kayıt Hatası",sonuc)

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