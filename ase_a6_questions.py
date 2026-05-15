questions = [
    {
        "q": "Technician A says that a digital multimeter set to the DC Volts position is used to check for voltage drop. Technician B says that a voltage drop test is performed with the circuit powered and the load turned on. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "Both",
        "explanation": "Voltage drop testing requires the circuit to be active and under load to measure resistance in the wiring."
    },
    {
        "q": "Technician A says that Ohm's law states that if resistance increases in a circuit with constant voltage, current flow will decrease. Technician B says that if voltage is doubled and resistance stays the same, current will double. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "Both",
        "explanation": "Current is directly proportional to voltage and inversely proportional to resistance (I = V / R)."
    },
    {
        "q": "Technician A says that a short-to-ground before the load will result in increased current flow and likely a blown fuse. Technician B says a short-to-ground after the load will cause the load to stay on regardless of the switch position. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "Both",
        "explanation": "A short before the load bypasses resistance, spiking current. A short after the load provides a constant ground path, bypassing the switch."
    },
    {
        "q": "Technician A says that a voltage drop of 0.1V across a connector is generally acceptable. Technician B says that all voltage drop tests should be performed with the component disconnected. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "A only",
        "explanation": "Voltage drop must be tested with the circuit 'loaded' (connected and ON). Disconnecting it shows open-circuit voltage, which is useless for this test."
    },
    {
        "q": "Technician A says that a CAN-Bus system uses two wires, CAN-High and CAN-Low, to communicate. Technician B says that the signals on these two wires are identical and in-phase. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "A only",
        "explanation": "CAN-Bus uses differential signaling; the voltages on CAN-H and CAN-L are mirrors of each other (out-of-phase) to cancel out noise."
    },
    {
        "q": "A vehicle with a slow-cranking complaint is being tested. Technician A says a starter current draw test should be performed first. Technician B says a battery voltage recovery test under load determines internal resistance. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "Both",
        "explanation": "High starter draw points to mechanical binding or a shorted starter motor, while battery load testing isolates whether the source can deliver adequate cranking amps."
    },
    {
        "q": "Technician A says that when testing an alternator output with an oscilloscope, a series of sharp downward spikes indicate an open diode. Technician B says a shorted diode will cause excessive AC ripple voltage on the multimeter. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "Both",
        "explanation": "An open diode drops output pattern segments on a scope, while a shorted diode leaks alternating current into the DC system, creating AC ripple."
    },
    {
        "q": "An open circuit fault in a standard three-wire linear potentiometer sensor circuit will cause what type of signal value return at the PCM signal line if the reference voltage line drops to ground?",
        "options": ["Steady 5.0V", "Hard 0.0V drop", "Floating variable voltage", "Blown sensor fuse"],
        "a": "Hard 0.0V drop",
        "explanation": "If the 5V reference line opens or shorts to ground before the sensor, the input signal line back to the controller loses all potential, registering a hard 0.0V signal drop."
    },
    {
        "q": "Technician A says that a parasitic current draw test should be performed with the ignition switch turned on. Technician B says that when checking parasitic draw, all vehicle modules must be allowed time to enter sleep mode. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "B only",
        "explanation": "Parasitic draw testing must be done with the key OFF. Modern network modules take up to 30-45 minutes to go to sleep; pulling fuses prematurely can wake them up."
    },
    {
        "q": "A brake light circuit fuse blows instantly whenever the brake pedal is depressed. Technician A says this indicates a short-to-ground in the power side of the circuit after the brake switch. Technician B says the problem is an open ground circuit at the tail light assembly. Who is right?",
        "options": ["A only", "B only", "Both", "Neither"],
        "a": "A only",
        "explanation": "An open ground causes the circuit to quit working entirely without blowing the fuse. An instant blown fuse when the switch closes confirms a dead short-to-ground on the load side."
    }
]
