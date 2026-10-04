# --------------------------------
# Gate state
# --------------------------------

gate_open = False


# --------------------------------
# Open gate
# --------------------------------

def open_gate():

    global gate_open

    if gate_open:
        return

    gate_open = True

    print("GATE OPENED")


# --------------------------------
# Close gate
# --------------------------------

def close_gate():

    global gate_open

    if not gate_open:
        return

    gate_open = False

    print("GATE CLOSED")


# --------------------------------
# Get current gate state
# --------------------------------

def is_gate_open():

    return gate_open


# --------------------------------
# Control gate
# --------------------------------

def control_gate(authorized):

    if authorized:
        open_gate()

    else:
        close_gate()


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    print("Testing gate controller...")

    print("\n--- Authorized ---")
    control_gate(True)

    print("\n--- Authorized again ---")
    control_gate(True)

    print("\n--- Unauthorized ---")
    control_gate(False)

    print("\n--- Unauthorized again ---")
    control_gate(False)