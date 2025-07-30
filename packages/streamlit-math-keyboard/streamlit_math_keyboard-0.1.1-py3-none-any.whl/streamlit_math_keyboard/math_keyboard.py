# streamlit_math_keyboard/math_keyboard.py
import os
import streamlit.components.v1 as components
import streamlit as st

# Determine the build directory for the frontend
_RELEASE = True # Set to False for development, True for production/PyPI

if not _RELEASE:
    _component_func = components.declare_component(
        "math_keyboard",
        url="http://localhost:5173" # Vite dev server URL (check your vite output)
        # If using parcel: url="http://localhost:1234"
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("math_keyboard", path=build_dir)

def math_keyboard(initial_value="", height=300, key=None):
    """
    Creates a new instance of the Math Keyboard component.

    Parameters
    ----------
    initial_value : str, optional
        The initial value to display in the keyboard's buffer.
    height : int, optional
        The height of the component iframe.
    key : str, optional
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the frontend and lose its current state.

    Returns
    -------
    str
        The current value entered into the math keyboard.
    """
    component_value = _component_func(
        initial_value=initial_value,
        height=height,
        key=key,
        default=initial_value # Default value if nothing is returned from frontend
    )
    return component_value

# Example usage (for testing directly)
if __name__ == "__main__":
    st.set_page_config(page_title="Math Keyboard Component Test", layout="centered")
    st.title("Math Keyboard Component Test")

    st.subheader("Interactive Keyboard")
    # Example 1: Basic usage
    current_expression = math_keyboard(key="keyboard1")
    st.markdown(f"Current Expression (keyboard1): ${current_expression}$", unsafe_allow_html=True)

    # st.subheader("Keyboard with Initial Value & Session State")
    # # Example 2: Using session state to persist value
    # if 'math_input_value' not in st.session_state:
    #     st.session_state.math_input_value = "123+456"

    # # The component's return value updates st.session_state.math_input_value
    # # because on_change is used.
    # # However, for custom components, the value is returned directly.
    # # We can assign it back to session state if needed.

    # # To make it truly interactive with session state, you'd typically
    # # pass the session state value in and update it based on the return.
    # # Streamlit's normal widgets handle this more directly with on_change.
    # # For custom components, the flow is:
    # # 1. Python sends initial_value.
    # # 2. JS sends back new value via setComponentValue.
    # # 3. Python function returns this new value.

    # ret_val = math_keyboard(
    #     initial_value=st.session_state.math_input_value,
    #     key="keyboard_stateful"
    # )

    # # If the returned value is different, update session state
    # # This can cause a double rerun if not careful, but shows the principle
    # if ret_val != st.session_state.math_input_value:
    #     st.session_state.math_input_value = ret_val
    #     # st.rerun() # Uncomment if you want immediate reflection of state change

    # st.write("Current Expression (keyboard_stateful from state):", st.session_state.math_input_value)

    # if st.button("Set keyboard_stateful to '99*11'"):
    #     st.session_state.math_input_value = "99*11"
    #     # st.rerun()

    st.info(f"""
    How this works:
    - The `math_keyboard` component is called.
    - Its `initial_value` is set from `st.session_state.math_input_value`.
    - When you type in the keyboard, the JavaScript sends the new value back to Python.
    - The `math_keyboard` function returns this new value.
    - We then update `st.session_state.math_input_value` with this returned value.
    """)