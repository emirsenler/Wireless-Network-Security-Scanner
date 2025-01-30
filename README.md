# Wireless-Network-Security-Scanner

# WiFi Ağ Güvenlik Analiz Aracı

WiFi ağlarını analiz eden ve potansiyel güvenlik tehditlerini tespit eden kapsamlı bir Python tabanlı araç. Bu araç, yakındaki kablosuz ağları tarar ve WPA analizi, evil twin tespiti ve sahte erişim noktası tanımlama gibi çeşitli güvenlik kontrolleri gerçekleştirir.

## Özellikler

- Ağ tarama ve bilgi toplama
- WPA/WPA2 güvenlik analizi
- Evil twin saldırı tespiti
- Sahte erişim noktası tespiti
- Detaylı JSON çıktı üretimi

## Gereksinimler

- Python 3.6+
- pywifi kütüphanesi
- Uyumlu bir kablosuz ağ arayüzü

## Kurulum

1. Bu projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/wifi-security-tool.git
cd wifi-security-tool
```

2. Sanal ortam oluşturun (opsiyonel ama önerilen):
```bash
python -m venv venv
# Windows için
venv\Scripts\activate
# Linux/Mac için
source venv/bin/activate
```

3. Gerekli kütüphaneleri yükleyin:
```bash
pip install pywifi
```

4. Linux sistemlerde root yetkileri gerekebilir:
```bash
sudo pip install pywifi
```

### Olası Kurulum Sorunları

1. Windows'ta pywifi kurulum hatası:
   - Visual C++ build tools yüklü olduğundan emin olun
   - Windows SDK'nın yüklü olduğundan emin olun

2. Linux'ta kurulum sorunları:
```bash
# Ubuntu/Debian için gerekli paketler
sudo apt-get update
sudo apt-get install python3-dev build-essential
sudo apt-get install libssl-dev libffi-dev
```

## Kullanım

1. Scripti çalıştırın:
```bash
python wifi_security.py
```

2. Script aşağıdaki işlemleri gerçekleştirecektir:
   - Yakındaki kablosuz ağları tarama
   - WPA/WPA2 güvenlik analizi
   - Olası evil twin saldırılarını kontrol etme
   - Olası sahte erişim noktalarını tespit etme

3. Sonuçlar `output.json` dosyasına kaydedilecektir

## Çıktı Formatı

Araç aşağıdaki yapıda bir JSON dosyası üretir:

```json
{
    "Networks": {
        "BSSID": {
            "SSID": "Ağ Adı",
            "Signal": -55,
            "Authentication": "WPA2-PSK",
            "Encryption": "WPA2",
            "Channel": 6
        }
    },
    "WPA_Analysis": {
        "BSSID": {
            "SSID": "Ağ Adı",
            "Secure": true,
            "Details": "WPA/WPA2 şifreleme aktif"
        }
    },
    "Evil_Twins": [
        {
            "SSID": "Ağ Adı",
            "Frequency": 2412,
            "BSSIDs": ["00:11:22:33:44:55", "AA:BB:CC:DD:EE:FF"],
            "Signal Difference": 20
        }
    ],
    "Rogue_APs": [
        {
            "SSID": "Ağ Adı",
            "BSSID": "00:11:22:33:44:55",
            "Signal Strength": -85,
            "Reason": "Zayıf sinyal - olası sahte AP"
        }
    ]
}
```

## Güvenlik Tehdidi Tespiti

### Evil Twin Tespiti
Evil twin saldırıları, bir saldırganın meşru bir ağı taklit eden sahte bir erişim noktası oluşturduğunda ortaya çıkar. Araç, potansiyel evil twin'leri şu şekilde tespit eder:
- Aynı SSID'ye sahip birden fazla erişim noktasını tanımlama
- Sinyal gücü farklılıklarını analiz etme
- Farklı üretici MAC adreslerini kontrol etme
- Frekans bantlarını karşılaştırma

### Sahte Erişim Noktası Tespiti
Sahte erişim noktaları (Rogue AP'ler), ağ güvenliğini tehlikeye atmak için kullanılabilecek yetkisiz erişim noktalarıdır. Araç, potansiyel sahte AP'leri şu şekilde tespit eder:
- Güvenilir BSSID'ler listesine karşı kontrol
- Sinyal gücü desenlerini analiz etme
- Gizli SSID'leri tanımlama
- Şüpheli yapılandırmaları işaretleme

## Hata Giderme

1. "No such interface" hatası:
   - Kablosuz ağ arayüzünüzün aktif olduğundan emin olun
   - `iwconfig` (Linux) veya `ipconfig` (Windows) ile arayüzü kontrol edin

2. Yetki hataları:
   - Linux'ta programı `sudo` ile çalıştırın
   - Windows'ta programı yönetici olarak çalıştırın

3. Tarama sonuçları boş:
   - Kablosuz ağ adaptörünüzün monitör modunu desteklediğinden emin olun
   - Farklı bir kablosuz ağ adaptörü denemeyi düşünün

## Katkıda Bulunma

Sorun bildirimleri ve geliştirme önerilerinizi gönderebilirsiniz!

## Güvenlik Notu

Bu araç, ağ yöneticileri ve güvenlik profesyonellerinin kendi ağlarını denetlemesi için tasarlanmıştır. Her zaman çevrenizdeki ağları taramak için gerekli izinlere sahip olduğunuzdan emin olun.

## Lisans

[MIT Lisansı](LICENSE)

## İletişim

Proje Sahibi - emirsenler


## Video

![Video](video/wifitool.gif)