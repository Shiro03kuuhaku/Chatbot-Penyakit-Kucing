import re
import random
import nltk
from nltk.chat.util import Chat, reflections
from spellchecker import SpellChecker


print("Program Chatbot AI")
sapaan = ["Hai juga", "Halo juga", "Halo", "Hai", "Apa Kabar"]

responses = {
    r"penyakit|sakit|kucing (mengalami|punya) (.*)": "Apa saja gejala yang ditunjukan oleh kucing anda?" ,
    r"kucing|sianosis|kulit|warna|kebiruan|batuk|sesak|napas|kelelahan (mengalami|punya) (.*)" : "Berdasarkan gejala yang diberikan kucing anda menderita penyakit Jantung Bawaan.\n" +
    "\tBeberapa kucing lahir dengan kelainan jantung bawaan yang dapat menyebabkan masalah kesehatan sepanjang hidup mereka. Gejalanya bervariasi tergantung pada jenis kelainan jantungnya. \n\t Pengelolaan tergantung pada tingkat keparahan, tetapi dapat mencakup pengobatan obat dan perubahan gaya hidup. \n\t Untuk lebih lanjut konsultasikan langsung ke dokter.",
    r"kehilangan|/bberat badan/b|muntah|diare|sering|buang|air|kecil|kencing|pipis|minum (mengalami|punya) (.*)" : "Beradsarkan gejala yang diberikan, kucing anda menderita penyakit Ginjal Kronis.\n"+
    "\t Penyakit ini adalah kondisi umum pada kucing yang lebih tua di mana fungsi ginjal menurun seiring waktu.\n\t Gejalanya mungkin tidak terlihat sampai penyakit mencapai tahap yang lebih lanjut. \n\t Pengelolaan meliputi diet khusus, terapi cairan, dan pengawasan teratur oleh dokter hewan.",
    r"kucing|muntah|/bnafsu makan/b|kehilangan|frekuensi|/buang air besar/b|meningkat|bab|dehidrasi|mulut|kering|mata|cekung (mengalami|punya) (.*)" : "Diare pada kucing adalah kondisi di mana kucing mengalami peningkatan frekuensi dan keencetan buang air besar, biasanya disertai dengan konsistensi tinja yang lebih lunak atau cair dari biasanya\n." +
    "\tPenyebab diare pada kucing bisa bermacam-macam, mulai dari perubahan diet, infeksi virus, bakteri, parasit, hingga kondisi medis yang lebih serius. \n\t Segera konsultasikan ke dokter hewan terdekat.",
    r"kucing|/bnafsu makan/b|hilang|sensitif|pada|cuaca|suhu|agresif (mengalami|punya) (.*)": "Berdasarkan gejala nampaknya kucing anda menderita penyakit Rabies. Rabies pada kucing adalah penyakit yang disebabkan oleh virus rabies\n." +
    "\tVirus ini dapat ditularkan kepada manusia dan hewan lain melalui gigitan atau kontak langsung dengan air liur hewan yang terinfeksi. \n\t Segera konsultasikan dengan dokter hewan jika Anda mencurigai hewan Anda terkena rabies.",
    r"kucing|\bkulit meradang\b|\bgatal-gatal parah\b|\bbulu rontok\b (mengalami|punya) (.*)": "Berdasarkan gejala yang anda berikan, nampaknya kucing anda menderita penyakit kutu kucing.\n" +
    "\t  Penyakit ini disebabkan oleh kutu. Kutu adalah parasit eksternal yang umum pada kucing.\n\t  Mereka adalah serangga kecil yang hidup di bulu dan kulit kucing, menghisap darah sebagai sumber makanan.\n"+
    "\t  Kutu dapat menyebabkan iritasi kulit yang parah, reaksi alergi, dan bahkan penularan penyakit seperti cacing dan bartonellosis (demam rayap).",
    r"kucing|\berat badan turun\b|\bkehilangan berat badan\b|\bmuntah-muntah\b|\bmuntah dan diare\b|\bkulit dan bulunya kusam\b|kulit|kusam|bulu (mengalami|punya|dan|,) (.*)": "Berdasarkan gejala yang anda berikan, nampaknya kucing anda menderita penyakit cacingan.\n"+
    "\t  Cacingan pada kucing adalah kondisi di mana kucing terinfeksi oleh cacing, baik itu cacing pita, cacing bulu, atau cacing tambang.\n"+
    "\t  Infeksi cacing pada kucing bisa terjadi karena kucing memakan telur cacing yang terkontaminasi di lingkungan, seperti dari tanah, air, atau makanan yang terinfeksi.\n" ,
    r"kucing|bersin|hidung|demam|batuk|memerah|mata|berair|hilang|kehilangan|makan|nafsu|\bkehilangan nafsu makan\b (mengalami|punya|dan|,) (.*)": "Berdasarkan gejala yang anda berikan nampaknya kucing anda terkena Flu Kucing.\n" +
    "\t  Penyakit flu pada kucing, juga dikenal sebagai Feline Upper Respiratory Infection (URI) atau Feline Viral Rhinotracheitis (FVR),\n\t  ini adalah penyakit umum yang disebabkan oleh virus\n." +
    "\t  Berikut adalah informasi lebih lanjut tentang penyakit flu kucing:\n\t  Penyebab: Penyebab utamanya adalah virus herpes felis (Feline Herpesvirus 1, FHV-1) dan calicivirus felis (Feline Calicivirus, FCV).\n"+
    "\t  Virus-virus ini menyebar melalui kontak langsung antara kucing yang terinfeksi dan kucing lainnya melalui bersin, batuk, atau kontak dengan sekresi hidung dan mata.",
    r"kucing|gusi|gusinya|memerah|kemerahan|bengkak|berdarah|\bnapas berbau tidak sedap\b|\bkesulitan makan\b|mengunyah (mengalami|punya|dan|,) (.*)": "Berdasarkan gejala yang anda berikan nampaknya kucing anda menderita Penyakit Gusi (Gingivitis atau Periodontitis)\n" +
    "\t  Penyakit gusi pada kucing, seperti gingivitis dan periodontitis, adalah masalah umum pada kucing.\n\t  Penyakit ini melibatkan peradangan atau infeksi pada gusi dan jaringan pendukung gigi.\n\t  Berikut adalah informasi lebih lanjut tentang penyakit gusi pada kucing:\n" +
    "\t  Penyebab: Gingivitis pada kucing sering disebabkan oleh penumpukan plak dan tartar di sekitar gusi. Bakteri dalam plak menyebabkan peradangan pada gusi.",
    r"kucing|muntah|diare|perut|\bnafsu makan menurun\b|kembung|sensitif (mengalami|punya|dan|,) (.*)" :"Berdasarkan gejala yang anda berikan nampaknya kucing anda menderita Penyakit Gastritis\n" +
    "\t  Penyakit Gastritis adalah peradangan pada lambung yang bisa disebabkan oleh banyak hal, termasuk infeksi bakteri, makanan yang tidak cocok, atau racun.\n\t  Kucing dengan gastritis mungkin akan muntah, memiliki diare (BAB yang encer), atau bahkan merasa sakit di perut mereka.\n\t  Berikut adalah solusi penanganan penyakit ini:\n" +
    "\t  Solusi: memberikan kucing makan makanan lunak atau khusus agar mudah dicerna, hindari memberikan makanan yang mengandung bahan-bahan yang berpotensi seperti racun.\n\t  Untuk lebih lanjutnya segera konsultasikan ke dokter hewan\n",
    r"kucing|Pembengkakan|yang|tidak|normal|penurunan|kehilangan|berat|badan|/bnafsu makan/b|lesu (mengalami|punya) (.*)" : "Berdasarkan gejala yang diberikan kucing anda menderita penyakit Kanker/n" +
    "\t Kucing juga dapat mengembangkan berbagai jenis kanker, termasuk limfoma, karsinoma sel basal, dan karsinoma sel skuamosa. /n/t Gejalanya bervariasi tergantung pada jenis kanker dan lokasinya. Pengobatan dapat melibatkan pembedahan, kemoterapi, atau radioterapi, tergantung pada kasusnya.",
}

p = ["Senang mendengarnya", "Syukurlah"]
q = ["Saya harap Anda baik-baik saja", "Semangat!", "Semoga Anda mendapat berita baik"]
w = ["Maaf, saya tidak paham", "Maaf, saya tidak mengerti"]
a = ["Sama-sama", "Tidak masalah, jika Anda memiliki pertanyaan lain, jangan ragu untuk bertanya.", "Senang bisa membantu ^^ jika anda memiliki pertanyaan lain, jangan ragu untuk bertanya"]
b = ["Ada yang bisa saya bantu?", "Apa keluhan Anda?"]
c = ["Apa yang bisa saya bantu?"]
g = ["Gejala apalagi yang terdapat pada kucing anda?"]
h = ["Apa saja gejala yang ditunjukan oleh kucing anda?"]
d = ["Baik, jika ada yang ingin ditanyakan, jangan ragu untuk bertanya."]

spell = SpellChecker(language='en')

def find_response(message):
    for pattern, response in responses.items():
        if re.search(pattern, message, re.IGNORECASE):
            return response
    return None

count = 0
symptoms = []
while True:
    x = input("User\t: ")
    if re.search(r'halo|hai|hello|hei|helo', x, re.IGNORECASE):
        print("Bot\t:", random.choice(sapaan))
    elif re.search(r'\btidak baik\b|\bsedang tidak baik\b|\bburuk\b', x, re.IGNORECASE):
        print("Bot\t:", random.choice(q))
    elif re.search(r'\btolong bantu saya\b|\bbantu saya\b|\bsaya ingin bertanya\b', x, re.IGNORECASE):
        print("Bot\t:", random.choice(c))
    elif re.search(r'\bbaik\b|\blumayan\b|\bkabar baik\b|\balhamdulillah\b', x, re.IGNORECASE):
        print("Bot\t:", random.choice(p))
    elif re.search(r'\bterima kasih\b|\bthanks\b|\bthank you\b', x, re.IGNORECASE):
        print("Bot\t:", random.choice(a))
    elif re.search(r'penyakit|sakit|kucing (mengalami|punya)', x,  re.IGNORECASE):
        print("Bot\t:", random.choice(h))
    elif re.search(r'\btidak ada\b|ngga|nggak|tidak', x, re.IGNORECASE):
        print("Bot\t:", random.choice(d))
    elif response := find_response(x):
      if len(x.split()) < 3:
          symptoms.append(x)
          count += 1
          if count < 3:
              print("Bot\t:", random.choice(g))
          else:
              diagnosis = find_response(' '.join(symptoms))
              print("Bot\t:", diagnosis)
      else:
          print("Bot\t:", response)
    else:
        corrected = ' '.join([spell.correction(word) for word in x.split()])
        print("Bot\t: Maaf, saya tidak paham. Apakah maksud Anda:", corrected, "?")
