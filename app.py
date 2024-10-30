import streamlit as st
import openai
from dotenv import load_dotenv
import os
import re

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
            max_tokens=800,
            temperature=creativity
        )
        
        # Ambil respons dan kembalikan
        exercise_content = response.choices[0].message['content'].strip()
        
        # Memisahkan soal dan jawaban sebagai daftar
        questions, answers = parse_exercise_and_answers(exercise_content, num_questions)
        
        return questions, answers
    
    except Exception as e:
        return f"Terjadi kesalahan: {e}", None

# Fungsi untuk memisahkan soal dan jawaban sebagai daftar
def parse_exercise_and_answers(content, num_questions):
    # Memisahkan soal dan jawaban menggunakan regex untuk memastikan soal dan jawaban sesuai
    questions = []
    answers = []
    
    # Gunakan regex untuk menangkap pola soal dan jawaban
    question_pattern = re.compile(r"\d+\.\s(.+?)(?=\d+\.|$)", re.DOTALL)  # Mencari tiap soal
    answer_pattern = re.compile(r"Jawaban:\s*(.+)", re.DOTALL)  # Mencari jawaban setelah kata "Jawaban:"

    # Cari soal dalam teks
    found_questions = question_pattern.findall(content)
    for q in found_questions:
        question_text = q.strip()
        if "Jawaban" in question_text:
            question, answer = question_text.split("Jawaban:", 1)
            questions.append(question.strip())
            answers.append(answer.strip())
        else:
            questions.append(question_text)
            answers.append("Jawaban tidak tersedia")  # Placeholder jika jawaban tidak ditemukan

    # Pastikan jumlah soal/jawaban sesuai dengan yang diminta
    questions = questions[:num_questions] + ["Soal tambahan"] * (num_questions - len(questions))
    answers = answers[:num_questions] + ["Jawaban tambahan"] * (num_questions - len(answers))
    
    return questions, answers

# Layout aplikasi Streamlit
st.title("🎓 Pembuat Latihan Bahasa Inggris Interaktif")

st.write("Aplikasi ini membantu guru membuat latihan Bahasa Inggris dengan berbagai jenis soal dan tingkat kesulitan.")

# Input teks dasar untuk latihan
text_input = st.text_area("Masukkan teks atau topik untuk latihan:", height=150)

# Dropdown untuk memilih jenis latihan
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
        questions, answers = generate_exercise(text_input, exercise_type, num_questions, difficulty, creativity)
        
        # Menampilkan soal dan jawaban secara terpisah dengan Expanders
        for idx, (question, answer) in enumerate(zip(questions, answers), 1):
            with st.expander(f"Soal {idx}"):
                st.markdown(f"**Soal:** {question}")
            with st.expander(f"Jawaban {idx}"):
                st.markdown(f"**Jawaban:** {answer}")
    else:
        st.warning("Silakan masukkan teks atau topik terlebih dahulu.")
