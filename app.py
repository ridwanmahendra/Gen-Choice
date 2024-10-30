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
            max_tokens=700,  # Token ditingkatkan untuk mencakup soal dan jawaban
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
st.title("LangChoice AI - Teknokrat")

st.write("Aplikasi ini membantu guru membuat latihan bahasa Inggris yang kompleks dan profesional dengan berbagai jenis soal dan tingkat kesulitan menggunakan AI")

# Input teks dasar untuk latihan
text_input = st.text_area("Masukkan teks atau topik untuk latihan:", height=200)

# Dropdown untuk memilih jenis latihan
exercise_type = st.selectbox(
    "Pilih jenis latihan:",
    ("Fill-in-the-Blank", "Multiple Choice", "Reading Comprehension")
)

# Input untuk jumlah soal
num_questions = st.number_input("Masukkan jumlah soal yang diinginkan:", min_value=1, max_value=10, value=3)

# Pilihan tingkat kesulitan
difficulty = st.selectbox(
    "Pilih tingkat kesulitan:",
    ("Mudah", "Sedang", "Sulit")
)

# Kontrol kreativitas (temperature)
creativity = st.slider("Atur tingkat kreativitas soal (0.0 = sangat tepat, 1.0 = sangat kreatif):", 0.0, 1.0, 0.7)

# Tombol untuk membuat latihan
if st.button("Buat Latihan"):
    if text_input:
        exercise, answers = generate_exercise(text_input, exercise_type, num_questions, difficulty, creativity)
        
        # Menampilkan soal dan jawaban secara terpisah
        st.write("**Latihan yang dihasilkan:**")
        st.write(exercise)
        
        st.write("**Jawaban:**")
        st.write(answers)
    else:
        st.write("Silakan masukkan teks atau topik terlebih dahulu.")
