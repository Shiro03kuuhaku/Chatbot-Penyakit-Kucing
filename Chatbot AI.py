import re
import random
import difflib

sapaan = ["Hai juga", "Halo juga", "Halo", "Hai", "Apa Kabar"]
p = ["Senang mendengarnya", "Syukurlah"]
q = ["Saya harap Anda baik-baik saja", "Semangat!", "Semoga Anda mendapat berita baik"]
w = ["Maaf, saya tidak paham", "Maaf, saya tidak mengerti"]
a = ["Sama-sama", "Tidak masalah", "Senang bisa membantu ^^ jika anda memiliki pertanyaan lain, jangan ragu untuk bertanya"]
c = ["Apa yang bisa saya bantu?"]
g = ["Gejala apalagi yang terdapat pada kucing anda?"]

kata_kunci = [
    "penyakit", "sakit", "kucing", "kulit", "gatal-gatal", "bulu", "berat badan",
    "diare", "muntah", "nafsu makan", "bersin", "demam", "batuk", "telinga",
    "gigi", "rabies", "kasih", "terima", "baik", "buruk", "bantu", "tolong"
]

solusi = {
    "rabies": (
        "\t Solusi: Segera hubungi dokter hewan dan jangan menangani kucing tanpa perlindungan. Jauhkan hewan dan orang lain dari kucing yang terinfeksi.\n"
        "\t Lakukan vaksinasi untuk kucing lain sebagai tindakan pencegahan."
    ),
    "diare": (
        "\t Solusi: Pastikan kucing tetap terhidrasi dengan memberikan air bersih. Berikan makanan mudah dicerna seperti makanan basah khusus kucing.\n"
        "\t Konsultasikan ke dokter hewan jika diare berlanjut lebih dari 24 jam."
    ),
    "kutu": (
        "\t  Solusi: Mandikan kucing dengan sampo anti-kutu khusus, gunakan sisir kutu, dan aplikasikan obat anti-kutu. \n"
        "\t  Bersihkan lingkungan kucing secara menyeluruh untuk mencegah infeksi ulang."
    ),
    "cacingan": (
        "\t Solusi: Berikan obat cacing sesuai rekomendasi dokter hewan. Jaga kebersihan lingkungan, termasuk tempat tidur dan litter box.\n"
        "\t Hindari kucing berburu atau makan hewan yang mungkin terinfeksi cacing."
    ),
    "gingivitis": (
        "\t Solusi: Sikat gigi kucing secara teratur dengan pasta gigi khusus. Berikan makanan kering yang membantu membersihkan plak.\n"
        "\t Segera konsultasikan ke dokter hewan jika gusi terlihat bengkak atau berdarah."
    ),
    "gastritis": (
        "\t Solusi: Berikan makanan lunak dan mudah dicerna. Hindari makanan yang dapat mengiritasi lambung. Pastikan kucing tetap terhidrasi.\n"
        "\t Konsultasikan ke dokter hewan jika gejala berlanjut."
    ),
    "flu kucing": (
        "\t Solusi: Berikan istirahat yang cukup di tempat yang hangat dan nyaman. Bersihkan mata dan hidung yang berair. \n"
        "\t Berikan makanan bergizi dan mudah dicerna. Konsultasikan ke dokter hewan jika tidak ada perbaikan."
    ),
    "infeksi telinga": (
        "\t Solusi: Bersihkan telinga dengan cairan pembersih khusus, dan gunakan obat tetes telinga yang diresepkan oleh dokter hewan.\n"
        "\t Hindari mengorek telinga terlalu dalam untuk mencegah cedera."
    ),
    "penyakit jantung": (
        "\t Solusi: Berikan makanan khusus untuk kesehatan jantung, jaga aktivitas kucing tetap moderat, dan konsultasikan "
        "\t dengan dokter hewan untuk pemeriksaan lebih lanjut."
    ),
    "masalah gigi": (
        "\t Solusi: Sikat gigi kucing secara teratur dengan pasta gigi khusus. Berikan makanan kering atau mainan kunyah untuk menjaga kebersihan gigi.\n"
        "\t Segera bawa kucing ke dokter hewan jika ada masalah pada giginya."
    )
}

respon = {
    r"penyakit|sakit|kucing (mengalami|punya) (.*)": (
        "Apa saja gejala yang ditunjukkan oleh kucing Anda?"
    ),
    r"kucing|kulit|iritasi|\bkulitnya memerah\b|\bkulit meradang\b|gatal-gatal|\bgatal-gatal parah\b|\bbulu rontok\b (mengalami|punya) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda menderita penyakit kutu kucing.\n"
        "\t Penyakit ini disebabkan oleh kutu. Kutu adalah parasit eksternal yang umum pada kucing.\n"
        "\t Mereka adalah serangga kecil yang hidup di bulu dan kulit kucing, menghisap darah sebagai sumber makanan.\n"
        "\t Kutu dapat menyebabkan iritasi kulit yang parah, reaksi alergi, dan bahkan penularan penyakit seperti cacing\n"
        "\t dan bartonellosis (demam rayap).\n\n" + solusi["kutu"]
    ),
    r"kucing|\berat badan turun\b|\bkehilangan berat badan\b|\bmuntah-muntah\b|\bmuntah dan diare\b|\bkulit dan bulunya kusam\b|kulit|kusam|bulu (mengalami|punya|dan|,) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda menderita penyakit cacingan.\n"
        "\tCacingan pada kucing adalah kondisi di mana kucing terinfeksi oleh cacing, baik itu cacing pita, "
        "cacing bulu, atau cacing tambang.\n"
        "\tInfeksi cacing pada kucing bisa terjadi karena kucing memakan telur cacing yang terkontaminasi "
        "di lingkungan, seperti dari tanah, air, atau makanan yang terinfeksi.\n\n" + solusi["cacingan"]
    ),
    r"kucing|\bdiare\b|\bmencret\b|\bkotorannya cair\b|\bpupnya berair\b|\bbuang air besar berair\b (mengalami|punya|dan|,) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda mengalami Diare.\n"
        "\tDiare pada kucing dapat disebabkan oleh berbagai faktor seperti perubahan diet, infeksi bakteri atau "
        "virus, parasit, atau reaksi alergi.\n"
        "\tKucing yang mengalami diare mungkin akan menunjukkan gejala seperti buang air besar yang lebih sering "
        "dari biasanya dengan konsistensi kotoran yang cair atau berair.\n\n" + solusi["diare"]
    ),
    r"kucing|muntah|perut|\bnafsu makan menurun\b|kembung|sensitif (mengalami|punya|dan|,) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda menderita Penyakit Gastritis.\n"
        "\tPenyakit Gastritis adalah peradangan pada lambung yang bisa disebabkan oleh banyak hal, termasuk "
        "infeksi bakteri, makanan yang tidak cocok, atau racun.\n"
        "\tKucing dengan gastritis mungkin akan muntah, memiliki diare (BAB yang encer), atau bahkan merasa "
        "sakit di perut mereka.\n\n" + solusi["gastritis"]
    ),
    r"kucing|bersin|hidung|demam|batuk|memerah|mata|berair|hilang|kehilangan|nafsu|makan|\bkehilangan nafsu makan\b (mengalami|punya|dan|,) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda terkena Flu Kucing.\n"
        "\tPenyakit flu pada kucing, juga dikenal sebagai Feline Upper Respiratory Infection (URI) atau "
        "Feline Viral Rhinotracheitis (FVR), \n"
        "\tini adalah penyakit umum yang disebabkan oleh virus.\n"
        "\tPenyebab: Penyebab utamanya adalah virus herpes felis (Feline Herpesvirus 1, FHV-1) dan "
        "calicivirus felis (Feline Calicivirus, FCV). \n"
        "\tVirus-virus ini menyebar melalui kontak langsung "
        "antara kucing yang terinfeksi dan kucing lainnya melalui bersin, batuk, atau kontak \n"
        "dengan sekresi hidung dan mata.\n\n" + solusi["flu kucing"]
    ),
    r"kucing|telinga|memerah|berdarah|\bkotoran telinga berlebihan\b|\bgatal-gatal parah\b|\bbulu rontok di sekitar telinga\b (mengalami|punya|dan|,) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda menderita Infeksi Telinga.\n"
        "\tInfeksi telinga pada kucing bisa disebabkan oleh bakteri, jamur, atau parasit seperti tungau.\n"
        "\tKucing dengan infeksi telinga mungkin akan sering menggaruk telinga mereka, menggelengkan kepala, "
        "atau memiliki bau tidak sedap dari telinga.\n\n" + solusi["infeksi telinga"]
    ),
    r"kucing|\bsulit bernafas\b|\bbatuk kering\b|\bkurang aktif\b|\bgusi pucat\b|\bperut bengkak\b (mengalami|punya|dan|,) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda menderita Penyakit Jantung.\n"
        "\tPenyakit jantung pada kucing bisa melibatkan berbagai kondisi seperti kardiomiopati atau kelainan "
        "pada katup jantung.\n"
        "\tGejalanya bisa meliputi sesak napas, batuk, dan kelelahan. Penyakit jantung pada kucing sering kali "
        "membutuhkan diagnosis dan perawatan khusus oleh dokter hewan.\n\n" + solusi["penyakit jantung"]
    ),
    r"kucing|\bgigi patah\b|\bmulut bau\b|\bsusah makan\b|\bsulit mengunyah makanan\b (mengalami|punya|dan|,) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda menderita masalah gigi.\n"
        "\tMasalah gigi pada kucing sering kali melibatkan gigi yang patah atau infeksi di dalam mulut.\n"
        "\tKucing yang mengalami masalah ini mungkin akan menunjukkan tanda-tanda seperti bau mulut, sulit makan, "
        "atau mengunyah dengan salah satu sisi mulut.\n\n" + solusi["masalah gigi"]
    ),
    r"kucing|rabies|\bbulunya berdiri\b|marah-marah|\bgampang marah\b|\bberperilaku agresif\b|kaku|kejang-kejang (mengalami|punya|dan|,) (.*)": (
        "Berdasarkan gejala yang Anda berikan, nampaknya kucing Anda mungkin menderita Rabies.\n"
        "\tRabies adalah penyakit virus yang sangat serius dan sering berakibat fatal, yang dapat mempengaruhi "
        "otak dan sistem saraf.\n"
        "\tKucing yang terinfeksi rabies bisa menunjukkan gejala seperti perubahan perilaku menjadi agresif, "
        "ketakutan pada air, dan kejang-kejang.\n\n" + solusi["rabies"]
    )
}

def autocorrect(kata):
    saran = difflib.get_close_matches(kata, kata_kunci)
    if saran:
        return saran[0]
    return kata

def proses_input(input):
    kata = input.split()
    kata_terkoreksi = [autocorrect(k) for k in kata]
    return ' '.join(kata_terkoreksi)

def cari_respon(pesan):
    for pattern, respons in respon.items():
        if re.search(pattern, pesan, re.IGNORECASE):
            return respons
    return None

print("=== Program Chatbot AI Diagnosis Penyakit Kucing ===")
print("Bot\t: Halo! selamat datang di progran kami, ada yang bisa kami bantu?")
while True:
    x = input("User\t: ")
    x = proses_input(x)
    if re.search(r'halo|hai|hello|hei|helo', x, re.IGNORECASE):
        print("Bot\t:", random.choice(sapaan))
    elif re.search(r'\btidak baik\b|\bsedang tidak baik\b|\bburuk\b', x, re.IGNORECASE):
        print("Bot\t:", random.choice(q))
    elif re.search(r'\btolong bantu saya\b|\bbantu saya\b|\bsaya ingin bertanya\b', x, re.IGNORECASE):
        print("Bot\t:", random.choice(c))
    elif re.search(r'baik|lumayan|\bkabar baik\b|\balhamdulillah\b', x, re.IGNORECASE):
        print("Bot\t:", random.choice(p))
    elif re.search(r'terima|kasih|\bthanks\b|\bthank you\b', x, re.IGNORECASE):
        print("Bot\t:", random.choice(a))
    elif respons := cari_respon(x):
      if len(x.split()) < 3:
            print("Bot\t:", random.choice(g))
      else:
            print("Bot\t:", respons)
    else:
        print("Bot\t:", random.choice(w))
