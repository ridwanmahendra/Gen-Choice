import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load API Key dari .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fungsi untuk memanggil OpenAI API dengan tipe latihan, jumlah soal, dan jawaban
def generate_exercise(prompt, exercise_type, num_questions, difficulty, creativity):
    try:
        # Prompt khusus untuk setiap jenis latihan dengan level kesulitan dan kreativitas
        prompt = f"Buat {num_questions} soal latihan bahasa Inggris dalam bentuk {exercise_type.lower()} berdasarkan teks berikut:\n\n{prompt}\n\n"
        prompt += f"Pastikan soalnya pada tingkat kesulitan {difficulty.lower()} dan sediakan jawaban lengkap untuk setiap soal.\n\nLatihan dan Jawaban:"

        # Panggilan API ke OpenAI dengan model gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kamu adalah asisten yang membantu membuat soal latihan Bahasa Inggris yang interaktif dan profesional."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=creativity
        )
        
        # Ambil respons dan kembalikan
        exercise_content = response.choices[0].message['content'].strip()
        
        # Memisahkan soal dan jawaban
        exercise, answers = parse_exercise_and_answers(exercise_content)
        return exercise, answers
    
    except Exception as e:
        return f"Terjadi kesalahan: {e}", None

# Fungsi untuk memisahkan soal dan jawaban
def parse_exercise_and_answers(content):
    # Coba memisahkan soal dan jawaban jika ada kata kunci pemisah (misalnya "Jawaban:" atau "Answers:")
    if "Jawaban:" in content:
        exercise, answers = content.split("Jawaban:", 1)
    elif "Answers:" in content:
        exercise, answers = content.split("Answers:", 1)
    else:
        exercise, answers = content, "Jawaban tidak ditemukan."
    
    return exercise.strip(), answers.strip()

# Layout aplikasi Streamlit
st.title("🎓 Pembuat Latihan Bahasa Inggris Interaktif")
st.write("Aplikasi ini membantu guru membuat latihan Bahasa Inggris yang kompleks dan profesional, dengan berbagai jenis soal dan tingkat kesulitan.")

# Styling CSS untuk tampilan yang lebih profesional
st.markdown("""
    <style>
        .stTextArea, .stSelectbox, .stNumberInput, .stSlider {
            background-color: #f0f2f6;
            padding: 8px;
        }
        .exercise-box {
            background-color: #eaf4f4;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
        }
        .answer-box {
            background-color: #f9f4ea;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Pengaturan kolom untuk elemen input agar lebih rapi
col1, col2 = st.columns(2)

# Input teks dasar untuk latihan
with col1:
    text_input = st.text_area("Masukkan teks atau topik untuk latihan:", height=150)

# Dropdown untuk memilih jenis latihan
with col2:
    exercise_type = st.selectbox(
        "Pilih jenis latihan:",
        ("Fill-in-the-Blank", "Multiple Choice", "Reading Comprehension")
    )

# Input untuk jumlah soal
num_questions = st.number_input("Jumlah soal yang diinginkan:", min_value=1, max_value=10, value=3)

# Pilihan tingkat kesulitan
difficulty = st.selectbox("Tingkat kesulitan:", ("Mudah", "Sedang", "Sulit"))

# Kontrol kreativitas (temperature)
creativity = st.slider("Tingkat kreativitas soal (0.0 = sangat tepat, 1.0 = sangat kreatif):", 0.0, 1.0, 0.7)

# Tombol untuk membuat latihan
if st.button("Buat Latihan"):
    if text_input:
        exercise, answers = generate_exercise(text_input, exercise_type, num_questions, difficulty, creativity)
        
        # Menampilkan soal dan jawaban dalam tampilan yang rapi dengan kotak
        st.write("### Latihan yang dihasilkan:")
        with st.expander("📄 Lihat Soal"):
            st.markdown(f"<div class='exercise-box'>{exercise}</div>", unsafe_allow_html=True)
        
        st.write("### Jawaban:")
        with st.expander("📝 Lihat Jawaban"):
            st.markdown(f"<div class='answer-box'>{answers}</div>", unsafe_allow_html=True)
            
    else:
        st.warning("Silakan masukkan teks atau topik terlebih dahulu.")
