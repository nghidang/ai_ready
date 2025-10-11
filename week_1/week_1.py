import openai
import streamlit as st

# Initialize OpenAI client
client = openai.OpenAI(
    base_url="https://aiportalapi.stu-platform.live/use",
    api_key="sk-amNWISclq5ZTRgAcgOBXzw"
)

# Streamlit app title
st.title("Meeting Transcript Summarizer")

# Chat input box
user_input = st.text_area("Enter the meeting transcript or prompt:", height=200)

# Button to submit the input
if st.button("Summarize"):
    if user_input:
        # Prepare the prompt
        prompt = f"""
        Summarize the key points and action items from the following meeting transcript in a concise and organized manner. 
        Focus on the main discussion points, decisions made, and specific tasks assigned to each attendee, including deadlines where applicable. 
        The meeting transcript:\n\n{user_input}
        """

        try:
            # Call the OpenAI API
            response = client.chat.completions.create(
                model="GPT-5-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            # Display the response
            st.subheader("Summary")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a transcript or prompt to summarize.")

# Optional: Add a clear button to reset the input
if st.button("Clear"):
    st.session_state.user_input = ""
    st.experimental_rerun()