"""
Opal Standard Library - Hardware Access / الوصول للهاردوير

Direct hardware access for system programming and IoT.
وصول مباشر للهاردوير لبرمجة الأنظمة وإنترنت الأشياء

Features / المميزات:
- CPU info / معلومات المعالج
- Memory info / معلومات الذاكرة
- Disk info / معلومات القرص
- Network info / معلومات الشبكة
- Battery (mobile) / البطارية
- GPIO (Raspberry Pi) / منافذ GPIO
- I2C / SPI / Serial / I2C / SPI / تسلسلي
- Temperature sensors / حساسات الحرارة
- USB devices / أجهزة USB

Works on Linux, Termux, Raspberry Pi
يعمل على Linux، Termux، Raspberry Pi
"""

import os
import sys
import platform
import subprocess
import struct


def get_module():
    """إرجاع دوال مكتبة الهاردوير / Return hardware module functions"""
    return {
        # CPU / المعالج
        'cpu_info': _cpu_info,
        'معلومات_المعالج': _cpu_info,
        'cpu_count': _cpu_count,
        'cpu_percent': _cpu_percent,
        'cpu_freq': _cpu_freq,

        # Memory / الذاكرة
        'memory_info': _memory_info,
        'معلومات_الذاكرة': _memory_info,
        'memory_total': _memory_total,
        'memory_used': _memory_used,
        'memory_free': _memory_free,
        'memory_percent': _memory_percent,

        # Disk / القرص
        'disk_info': _disk_info,
        'معلومات_القرص': _disk_info,
        'disk_usage': _disk_usage,

        # Network / الشبكة
        'network_info': _network_info,
        'معلومات_الشبكة': _network_info,
        'ip_address': _ip_address,
        'mac_address': _mac_address,
        'hostname': _hostname,

        # Battery (Termux/mobile) / البطارية
        'battery_level': _battery_level,
        'مستوى_البطارية': _battery_level,
        'battery_status': _battery_status,
        'is_charging': _is_charging,

        # Temperature / الحرارة
        'cpu_temp': _cpu_temp,
        'حرارة_المعالج': _cpu_temp,

        # GPIO (Raspberry Pi) / منافذ GPIO
        'gpio_setup': _gpio_setup,
        'gpio_read': _gpio_read,
        'gpio_write': _gpio_write,

        # File system / نظام الملفات
        'mounts': _mounts,
        'الأقراص_المركبة': _mounts,

        # USB / USB
        'usb_devices': _usb_devices,

        # Display / الشاشة
        'screen_brightness': _screen_brightness,
        'سطوع_الشاشة': _screen_brightness,

        # Vibration (mobile) / الاهتزاز
        'vibrate': _vibrate,
        'اهتزاز': _vibrate,

        # Camera (mobile) / الكاميرا
        'take_photo': _take_photo,
        'التقط_صورة': _take_photo,

        # Notifications (mobile) / الإشعارات
        'notify': _notify,
        'إشعار': _notify,

        # Clipboard / الحافظة
        'clipboard_get': _clipboard_get,
        'clipboard_set': _clipboard_set,

        # System / النظام
        'uptime': _uptime,
        'boot_time': _boot_time,
    }


# ==============================================================
# CPU / المعالج
# ==============================================================

def _cpu_info():
    """معلومات المعالج / CPU info"""
    info = {
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'cores': os.cpu_count(),
        'python_version': platform.python_version(),
        'system': platform.system(),
        'release': platform.release(),
    }

    # Try to get CPU model on Linux / محاولة الحصول على نموذج المعالج
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('model name'):
                    info['model'] = line.split(':')[1].strip()
                    break
    except:
        pass

    return info


def _cpu_count():
    """عدد أنوية المعالج / CPU core count"""
    return os.cpu_count() or 1


def _cpu_percent():
    """نسبة استخدام المعالج / CPU usage percent"""
    try:
        # Get CPU usage from /proc/stat / الحصول على الاستخدام من /proc/stat
        with open('/proc/stat', 'r') as f:
            line = f.readline()
        parts = line.split()[1:]
        # user, nice, system, idle, etc.
        total = sum(int(x) for x in parts)
        idle = int(parts[3])
        # Sample again after a delay / أخذ عينة أخرى بعد تأخير
        import time
        time.sleep(0.1)
        with open('/proc/stat', 'r') as f:
            line = f.readline()
        parts2 = line.split()[1:]
        total2 = sum(int(x) for x in parts2)
        idle2 = int(parts2[3])
        # Calculate percentage / حساب النسبة
        total_diff = total2 - total
        idle_diff = idle2 - idle
        if total_diff > 0:
            return round(100 * (1 - idle_diff / total_diff), 1)
    except:
        pass
    return 0


def _cpu_freq():
    """تردد المعالج / CPU frequency"""
    try:
        with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r') as f:
            return int(f.read().strip()) / 1000  # Convert to MHz
    except:
        pass
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('cpu MHz'):
                    return float(line.split(':')[1].strip())
    except:
        pass
    return 0


# ==============================================================
# Memory / الذاكرة
# ==============================================================

def _memory_info():
    """معلومات الذاكرة / Memory info"""
    info = {'total': 0, 'used': 0, 'free': 0, 'percent': 0}
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal'):
                    info['total'] = int(line.split()[1]) * 1024  # KB to bytes
                elif line.startswith('MemAvailable'):
                    info['free'] = int(line.split()[1]) * 1024
                    break
        info['used'] = info['total'] - info['free']
        if info['total'] > 0:
            info['percent'] = round(100 * info['used'] / info['total'], 1)
    except:
        pass
    return info


def _memory_total():
    return _memory_info().get('total', 0)


def _memory_used():
    return _memory_info().get('used', 0)


def _memory_free():
    return _memory_info().get('free', 0)


def _memory_percent():
    return _memory_info().get('percent', 0)


# ==============================================================
# Disk / القرص
# ==============================================================

def _disk_info():
    """معلومات القرص / Disk info"""
    result = []
    try:
        df = subprocess.run(['df', '-h'], capture_output=True, text=True)
        for line in df.stdout.split('\n')[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    result.append({
                        'filesystem': parts[0],
                        'size': parts[1],
                        'used': parts[2],
                        'available': parts[3],
                        'percent': parts[4],
                        'mount': parts[5],
                    })
    except:
        pass
    return result


def _disk_usage(path='/'):
    """استخدام القرص / Disk usage for path"""
    try:
        st = os.statvfs(path)
        total = st.f_blocks * st.f_frsize
        free = st.f_bavail * st.f_frsize
        used = total - free
        return {
            'total': total,
            'used': used,
            'free': free,
            'percent': round(100 * used / total, 1) if total > 0 else 0,
        }
    except:
        return {'total': 0, 'used': 0, 'free': 0, 'percent': 0}


# ==============================================================
# Network / الشبكة
# ==============================================================

def _network_info():
    """معلومات الشبكة / Network info"""
    interfaces = {}
    try:
        # Get interfaces from /proc/net or ifconfig
        result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
        if result.returncode == 0:
            current_iface = None
            for line in result.stdout.split('\n'):
                if line and line[0].isdigit():
                    parts = line.split()
                    current_iface = parts[1].rstrip(':')
                    interfaces[current_iface] = {'ip': None, 'mac': None}
                elif 'inet ' in line and current_iface:
                    ip = line.split('inet ')[1].split('/')[0]
                    interfaces[current_iface]['ip'] = ip
                elif 'link/ether' in line and current_iface:
                    mac = line.split('link/ether ')[1].split()[0]
                    interfaces[current_iface]['mac'] = mac
    except:
        pass
    return interfaces


def _ip_address():
    """عنوان IP / IP address"""
    info = _network_info()
    for iface, data in info.items():
        if data.get('ip') and not data['ip'].startswith('127.'):
            return data['ip']
    return '127.0.0.1'


def _mac_address():
    """عنوان MAC / MAC address"""
    info = _network_info()
    for iface, data in info.items():
        if data.get('mac'):
            return data['mac']
    return ''


def _hostname():
    """اسم المضيف / Hostname"""
    try:
        return subprocess.run(['hostname'], capture_output=True, text=True).stdout.strip()
    except:
        return os.uname().nodename if hasattr(os, 'uname') else 'unknown'


# ==============================================================
# Battery (mobile/Termux) / البطارية
# ==============================================================

def _battery_level():
    """مستوى البطارية / Battery level (0-100)"""
    # Try Termux API first / تجربة Termux API أولاً
    try:
        result = subprocess.run(
            ['termux-battery-status'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return data.get('percentage', -1)
    except:
        pass

    # Try /sys/class/power_supply / تجربة /sys/class/power_supply
    try:
        for bat_dir in ['/sys/class/power_supply/BAT0', '/sys/class/power_supply/battery']:
            if os.path.exists(bat_dir):
                with open(f'{bat_dir}/capacity', 'r') as f:
                    return int(f.read().strip())
    except:
        pass

    return -1


def _battery_status():
    """حالة البطارية / Battery status"""
    try:
        result = subprocess.run(
            ['termux-battery-status'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
    except:
        pass

    try:
        for bat_dir in ['/sys/class/power_supply/BAT0', '/sys/class/power_supply/battery']:
            if os.path.exists(bat_dir):
                with open(f'{bat_dir}/status', 'r') as f:
                    return {'status': f.read().strip()}
    except:
        pass
    return {'status': 'unknown'}


def _is_charging():
    """هل البطارية مشحونة؟ / Is charging?"""
    status = _battery_status()
    s = status.get('status', '') if isinstance(status, dict) else str(status)
    return 'charging' in str(s).lower()


# ==============================================================
# Temperature / الحرارة
# ==============================================================

def _cpu_temp():
    """حرارة المعالج / CPU temperature"""
    # Try /sys/class/thermal / تجربة /sys/class/thermal
    try:
        for i in range(5):
            path = f'/sys/class/thermal/thermal_zone{i}/temp'
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return int(f.read().strip()) / 1000  # Convert to Celsius
    except:
        pass

    # Try vcgencmd (Raspberry Pi) / تجربة vcgencmd
    try:
        result = subprocess.run(
            ['vcgencmd', 'measure_temp'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            temp_str = result.stdout.split('=')[1].split("'")[0]
            return float(temp_str)
    except:
        pass

    return -1


# ==============================================================
# GPIO (Raspberry Pi) / منافذ GPIO
# ==============================================================

def _gpio_setup(pin, mode='out'):
    """إعداد منفذ GPIO / Setup GPIO pin"""
    try:
        # Try using /sys/class/gpio / تجربة /sys/class/gpio
        gpio_dir = f'/sys/class/gpio/gpio{pin}'
        if not os.path.exists(gpio_dir):
            with open('/sys/class/gpio/export', 'w') as f:
                f.write(str(pin))
        with open(f'{gpio_dir}/direction', 'w') as f:
            f.write(mode)
        return True
    except:
        pass

    # Try via subprocess / تجربة عبر subprocess
    try:
        if subprocess.run(['gpio', 'mode', str(pin), mode]).returncode == 0:
            return True
    except:
        pass

    return False


def _gpio_read(pin):
    """قراءة من GPIO / Read from GPIO"""
    try:
        with open(f'/sys/class/gpio/gpio{pin}/value', 'r') as f:
            return int(f.read().strip())
    except:
        try:
            result = subprocess.run(['gpio', 'read', str(pin)], capture_output=True, text=True)
            return int(result.stdout.strip())
        except:
            return -1


def _gpio_write(pin, value):
    """الكتابة لـ GPIO / Write to GPIO"""
    try:
        with open(f'/sys/class/gpio/gpio{pin}/value', 'w') as f:
            f.write(str(value))
        return True
    except:
        try:
            subprocess.run(['gpio', 'write', str(pin), str(value)])
            return True
        except:
            return False


# ==============================================================
# File system / نظام الملفات
# ==============================================================

def _mounts():
    """الأقراص المركبة / Mounted filesystems"""
    mounts = []
    try:
        with open('/proc/mounts', 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 4:
                    mounts.append({
                        'device': parts[0],
                        'mount_point': parts[1],
                        'type': parts[2],
                        'options': parts[3],
                    })
    except:
        pass
    return mounts


# ==============================================================
# USB / USB
# ==============================================================

def _usb_devices():
    """أجهزة USB / USB devices"""
    devices = []
    try:
        result = subprocess.run(['lsusb'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if line.strip():
                devices.append(line.strip())
    except:
        pass
    return devices


# ==============================================================
# Display / الشاشة
# ==============================================================

def _screen_brightness(level=None):
    """سطوع الشاشة / Screen brightness (0-100)"""
    if level is not None:
        # Set brightness / ضبط السطوع
        try:
            # Termux / Termux
            subprocess.run(['termux-brightness', str(int(level))])
            return level
        except:
            pass
        try:
            # Linux / Linux
            with open('/sys/class/backlight/intel_backlight/brightness', 'w') as f:
                max_bright = 255
                with open('/sys/class/backlight/intel_backlight/max_brightness', 'r') as mf:
                    max_bright = int(mf.read().strip())
                f.write(str(int(level * max_bright / 100)))
        except:
            pass
        return level
    else:
        # Get brightness / الحصول على السطوع
        try:
            with open('/sys/class/backlight/intel_backlight/brightness', 'r') as f:
                bright = int(f.read().strip())
            with open('/sys/class/backlight/intel_backlight/max_brightness', 'r') as f:
                max_bright = int(f.read().strip())
            return round(100 * bright / max_bright, 1)
        except:
            return -1


# ==============================================================
# Vibration (mobile) / الاهتزاز
# ==============================================================

def _vibrate(duration=500):
    """اهتزاز الجهاز / Vibrate device"""
    try:
        subprocess.run(['termux-vibrate', '-d', str(duration)])
        return True
    except:
        return False


# ==============================================================
# Camera (mobile) / الكاميرا
# ==============================================================

def _take_photo(path='photo.jpg'):
    """التقاط صورة / Take photo"""
    try:
        subprocess.run(['termux-camera-photo', path])
        return path
    except:
        return None


# ==============================================================
# Notifications (mobile) / الإشعارات
# ==============================================================

def _notify(title, message=''):
    """إرسال إشعار / Send notification"""
    try:
        subprocess.run(['termux-notification', '--title', str(title), '--content', str(message)])
        return True
    except:
        # Fallback: just print / احتياطي: طباعة فقط
        print(f'🔔 {title}: {message}')
        return False


# ==============================================================
# Clipboard / الحافظة
# ==============================================================

def _clipboard_get():
    """الحصول على محتوى الحافظة / Get clipboard content"""
    try:
        result = subprocess.run(['termux-clipboard-get'], capture_output=True, text=True)
        return result.stdout
    except:
        try:
            result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'],
                                    capture_output=True, text=True)
            return result.stdout
        except:
            return ''


def _clipboard_set(text):
    """تعيين محتوى الحافظة / Set clipboard content"""
    try:
        subprocess.run(['termux-clipboard-set', str(text)])
        return True
    except:
        try:
            subprocess.run(['xclip', '-selection', 'clipboard'], input=str(text), text=True)
            return True
        except:
            return False


# ==============================================================
# System / النظام
# ==============================================================

def _uptime():
    """وقت التشغيل / System uptime (seconds)"""
    try:
        with open('/proc/uptime', 'r') as f:
            return float(f.read().split()[0])
    except:
        return 0


def _boot_time():
    """وقت الإقلاع / Boot time"""
    try:
        with open('/proc/stat', 'r') as f:
            for line in f:
                if line.startswith('btime'):
                    return int(line.split()[1])
    except:
        pass
    return 0
