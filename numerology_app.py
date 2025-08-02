import streamlit as st
from datetime import datetime


# 🔁 Utility Functions
def reduce_to_single_digit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def get_lucky_and_avoid_numbers(num):
    table = {
        1: {'lucky': [1, 2, 3, 4, 5, 7, 9], 'avoid': [6, 8]},
        2: {'lucky': [1, 3, 4, 7, 8, 9], 'avoid': [2, 5, 6]},
        3: {'lucky': [1, 2, 3, 5, 6, 8, 9], 'avoid': [4, 7]},
        4: {'lucky': [1, 2, 5, 6, 7, 9], 'avoid': [3, 4, 8]},
        5: {'lucky': [1, 3, 4, 5, 6, 7, 8, 9], 'avoid': [2]},
        6: {'lucky': [3, 4, 5, 8, 9], 'avoid': [1, 2, 6, 7]},
        7: {'lucky': [1, 2, 3, 4, 5, 6, 7, 9], 'avoid': [8]},
        8: {'lucky': [1, 3, 5, 6, 8, 9], 'avoid': [2, 4, 7]},
        9: {'lucky': [1, 2, 3, 4, 5, 6, 9], 'avoid': [7, 8]}
    }
    return table.get(num, {'lucky': [], 'avoid': []})


# 🎨 Sidebar Navigation
st.sidebar.title("🔢 Numerology Navigator")
st.sidebar.markdown("Use this tool to find lucky numbers based on your DOB and mobile.")

section = st.sidebar.radio("Choose Section", ["Overview", "Check Lucky Numbers", "Evaluate Mobile Number"])

# 🏠 Overview Section
if section == "Overview":
    st.title("📿 Mobile Number Numerology Advisor")
    st.markdown("""
        Welcome to your personal numerology dashboard!  
        Understand how your birth energies align with mobile vibrations 🌟  
        Navigate through tabs to begin your exploration.
    """)
    st.image("E:\Projects\PyCharm\mobile\img\img1.png",width=100)

# 🔍 Check Lucky Numbers Section
elif section == "Check Lucky Numbers":
    st.title("🔍 Discover Your Lucky Numbers")

    default_dob = datetime(1990, 1, 1)
    dob = st.date_input("Select your Date of Birth", value=default_dob, min_value=datetime(1900, 1, 1),
                        max_value=datetime.today())
    if dob > datetime.today().date():
        st.error("Date of Birth cannot be in the future.")
    else:
        birth_number = reduce_to_single_digit(dob.day)
        life_path_number = reduce_to_single_digit(sum(map(int, str(dob.day) + str(dob.month) + str(dob.year))))

        birth_data = get_lucky_and_avoid_numbers(birth_number)
        life_data = get_lucky_and_avoid_numbers(life_path_number)

        common_lucky = sorted(set(birth_data['lucky']) & set(life_data['lucky']))
        common_avoid = sorted(set(birth_data['avoid']) & set(life_data['avoid']))

        st.subheader("🎯 Numerology Breakdown")
        st.table({
            "Number Type": ["Birth (Psychic)", "Life Path", "Common Lucky", "Overlapping Avoid"],
            "Value": [birth_number, life_path_number, "-", "-"],
            "Lucky Numbers": [", ".join(map(str, birth_data['lucky'])), ", ".join(map(str, life_data['lucky'])),
                              ", ".join(map(str, common_lucky)), "-"],
            "Avoid Numbers": [", ".join(map(str, birth_data['avoid'])), ", ".join(map(str, life_data['avoid'])), "-",
                              ", ".join(map(str, common_avoid)) if common_avoid else "None 🎉"]
        })

# 📱 Mobile Number Section
elif section == "Evaluate Mobile Number":
    st.title("📱 Check Mobile Number Vibrational Match")

    mobile = st.text_input("Enter a 10-digit Mobile Number")
    if mobile and len(mobile) == 10 and mobile.isdigit():
        mobile_vibration = reduce_to_single_digit(sum(map(int, mobile)))
        st.write(f"**Mobile Number Vibration:** {mobile_vibration}")

        # Cross-match
        birth_number = reduce_to_single_digit(datetime.today().day)  # fallback if user skips DOB
        life_path_number = reduce_to_single_digit(
            sum(map(int, str(datetime.today().day) + str(datetime.today().month) + str(datetime.today().year))))
        birth_lucky = get_lucky_and_avoid_numbers(birth_number)['lucky']
        life_lucky = get_lucky_and_avoid_numbers(life_path_number)['lucky']

        if mobile_vibration in birth_lucky or mobile_vibration in life_lucky:
            st.success("✅ This mobile number is numerologically favorable!")
        else:
            st.warning("⚠️ Consider choosing a number closer to your lucky vibrations.")
    elif mobile:
        st.error("🚫 Please enter a valid 10-digit number.")

    st.markdown("_Tip: Numbers ending in 6 or 9 often resonate positively. Avoid excessive 0s or repeated 8s._")