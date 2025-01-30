import json
import time
from pywifi import PyWiFi, const, Profile

def scan_networks():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(5)
    scan_results = iface.scan_results()
    
    networks = {}
    for network in scan_results:
        ssid = network.ssid
        bssid = network.bssid
        signal = network.signal
        akm = network.akm
        freq = network.freq
        
        channel = (freq - 2407) // 5 if freq < 5000 else (freq - 5000) // 5

        encryption_name = "WPA2-PSK" if akm and const.AKM_TYPE_WPA2PSK in akm else "WPA-PSK" if akm and const.AKM_TYPE_WPA in akm else "WEP"

        networks[bssid] = {
            "SSID": ssid,
            "Signal": signal,
            "Encryption": encryption_name,
            "Channel": channel
        }
    return networks

def analyze_wpa(networks):
    analysis = {}
    for bssid, info in networks.items():
        if "WPA" in info["Encryption"] or "WPA2" in info["Encryption"]:
            analysis[bssid] = {
                "SSID": info["SSID"],
                "Secure": True,
                "Details": "WPA/WPA2 şifreleme aktif."
            }
        else:
            analysis[bssid] = {
                "SSID": info["SSID"],
                "Secure": False,
                "Details": "Şifreleme aktif değil veya zayıf."
            }
    return analysis

def get_vendor_from_bssid(bssid):
    return ":".join(bssid.split(":")[:3])

def detect_evil_twin(networks):
    ssid_channels = {}
    evil_twins = []

    for bssid, info in networks.items():
        ssid = info["SSID"]
        channel = info["Channel"]
        signal = info["Signal"]

        freq = info.get("Freq", None)

        if not ssid or channel is None:
            continue

        if (ssid, freq) not in ssid_channels:
            ssid_channels[(ssid, freq)] = []
        ssid_channels[(ssid, freq)].append((bssid, signal))

    for (ssid, freq), bssid_signal_list in ssid_channels.items():
        if len(bssid_signal_list) > 1:
            bssids = [item[0] for item in bssid_signal_list]
            signals = [item[1] for item in bssid_signal_list]
            
            vendors = {get_vendor_from_bssid(b) for b in bssids}
            
            max_signal = max(signals)
            min_signal = min(signals)
            signal_difference = abs(max_signal - min_signal)

            if len(vendors) > 1 or signal_difference > 15:
                evil_twins.append({
                    "SSID": ssid,
                    "Frequency": freq if freq else "N/A",
                    "BSSIDs": bssids,
                    "Signal Difference": signal_difference
                })

    filtered_evil_twins = []
    for item in evil_twins:
        if len(item['BSSIDs']) > 1:
            first_vendor = get_vendor_from_bssid(item['BSSIDs'][0])
            if all(get_vendor_from_bssid(b) != first_vendor for b in item['BSSIDs'][1:]):
                filtered_evil_twins.append(item)
    
    return filtered_evil_twins

def detect_rogue_ap(networks, trusted_bssids):
    rogue_aps = []

    for bssid, info in networks.items():
        ssid = info["SSID"]
        signal = info["Signal"]

        if not ssid:
            rogue_aps.append({"SSID": "(Gizli SSID)", "BSSID": bssid})
            continue
        
        if bssid not in trusted_bssids:
            if signal < -80:
                rogue_aps.append({
                    "SSID": ssid,
                    "BSSID": bssid,
                    "Signal Strength": signal,
                    "Reason": "Zayıf sinyal - olası rogue AP"
                })
            else:
                rogue_aps.append({"SSID": ssid, "BSSID": bssid, "Signal Strength": signal})

    return rogue_aps

def main():
    print("Kablosuz ağ taraması yapılıyor...")
    networks = scan_networks()

    print("WPA/WPA2 analizi yapılıyor...")
    wpa_analysis = analyze_wpa(networks)

    print("Evil twin kontrolü yapılıyor...")
    evil_twins = detect_evil_twin(networks)

    print("Rogue AP kontrolü yapılıyor...")
    trusted_bssids = ["00:11:22:33:44:55"]
    rogue_aps = detect_rogue_ap(networks, trusted_bssids)

    result = {
        "Networks": networks,
        "WPA_Analysis": wpa_analysis,
        "Evil_Twins": evil_twins,
        "Rogue_APs": rogue_aps
    }

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Analiz tamamlandı. Sonuçlar 'output.json' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()