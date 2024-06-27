import streamlit as st
from model import getResponse

def main():
    st.set_page_config(page_title="Beautiful Chatbot", page_icon=":speech_balloon:")
    st.title("Welcome to My SQL chatbot 🌱,Powered by Pratik")
    st.markdown("---")
    st.write("Feel free to chat with your databases:")
    
    user_input = st.text_area("Type your message here:", height=100)

    if st.button("Send"):
        if user_input:
            response = getResponse(user_input)
            st.markdown("---")
            st.write("Response:")
            st.write(response)
        else:
            st.warning("Please type a message before sending.")

    if st.button("Refresh"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
