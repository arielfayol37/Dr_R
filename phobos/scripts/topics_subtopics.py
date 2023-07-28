from phobos.models import Topic, SubTopic
def run():
    # Define a dictionary with topics and their subtopics
    topics_subtopics = {
        'Mechanics': [
            'Kinematics',
            'Newton\'s Laws of Motion',
            'Work and Energy',
            'Momentum and Collisions',
            'Circular Motion',
            'Oscillations',
            'Gravitation',
            'Fluid Mechanics',
            'Statics and Dynamics of Rigid Bodies',
        ],
        'Thermodynamics': [
            'Thermal Equilibrium',
            'Laws of Thermodynamics',
            'Heat Transfer',
            'Thermodynamic Processes',
            'Entropy and Carnot Cycle',
            'Heat Engines',
        ],
        'Electricity and Magnetism': [
            'Electric Charge and Electric Field',
            'Gauss\'s Law',
            'Electric Potential and Capacitance',
            'Current and Resistance',
            'Ohm\'s Law and Circuits',
            'Magnetic Fields and Forces',
            'Electromagnetic Induction',
            'AC and DC Circuits',
            'Maxwell\'s Equations',
        ],
        'Waves and Optics': [
            'Wave Properties',
            'Wave Equation',
            'Superposition of Waves',
            'Interference and Diffraction',
            'Polarization of Light',
            'Doppler Effect',
            'Geometric Optics',
            'Lens and Mirrors',
            'Wave Optics',
        ],
        'Modern Physics': [
            'Quantum Mechanics',
            'Dual Nature of Matter and Radiation',
            'Atomic Models',
            'Nuclear Physics',
            'Special Theory of Relativity',
            'Particle Physics',
            'Cosmology',
        ],
        'Fluid Mechanics': [
            'Properties of Fluids',
            'Fluid Statics',
            'Bernoulli\'s Equation',
            'Fluid Dynamics',
            'Viscosity',
            'Surface Tension',
            'Turbulence',
        ],
        'Oscillations and Waves': [
            'Simple Harmonic Motion',
            'Damped Oscillations',
            'Forced Oscillations',
            'Waves in Strings and Pipes',
            'Sound Waves',
            'Standing Waves',
            'Resonance',
        ],
        'Optics and Light': [
            'Geometric Optics',
            'Lens and Mirrors',
            'Wave Optics',
            'Interference and Diffraction',
            'Polarization of Light',
            'Dispersion of Light',
            'Speed of Light and Index of Refraction',
            'Ray Optics in Nature (Rainbows, Mirages, etc.)',
            'Optical Instruments (Microscopes, Telescopes)',
        ]
    }

    # Create instances of subtopics using nested for loops and the dictionary values
    for topic_name, subtopics in topics_subtopics.items():
        # Check if the topic already exists in the database
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        # If the topic was just created, print a message
        if created:
            print(f"Created new topic: {topic_name}")
        
        for subtopic_name in subtopics:
            SubTopic.objects.create(topic=topic, name=subtopic_name)

    # Verify the creation of objects
    print(Topic.objects.all())
    print(SubTopic.objects.all())
