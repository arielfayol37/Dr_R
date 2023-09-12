from phobos.models import Topic, SubTopic

def run():
    # Define a dictionary with topics and their subtopics
    topics_subtopics = {
        'Mechanics': [
            'Kinematics',
            'Newton\'s Laws of Motion',
            'Work, Energy, and Power',
            'Momentum and Collisions',
            'Circular and Rotational Motion',
            'Gravitation',
            'Statics of Rigid Bodies',
            'Dynamics of Rigid Bodies',
        ],
        'Thermodynamics': [
            'Thermal Properties of Matter',
            'Thermal Equilibrium and Temperature',
            'First Law of Thermodynamics',
            'Second Law of Thermodynamics',
            'Heat Transfer Methods',
            'Thermodynamic Processes',
            'Entropy and Carnot Cycle',
            'Heat Engines and Refrigerators',
        ],
        'Electricity and Magnetism': [
            'Electrostatics',
            'Electric Potential and Capacitance',
            'Current Electricity',
            'Magnetic Effects of Current',
            'Electromagnetic Induction and AC',
            'Electromagnetic Waves',
            'Maxwell\'s Equations',
        ],
        'Waves': [
            'Wave Basics and Types',
            'Wave Properties and Behavior',
            'Superposition and Standing Waves',
            'Sound Waves',
            'Doppler Effect',
            'Resonance',
        ],
        'Optics': [
            'Reflection and Refraction',
            'Lens, Mirrors, and Optical Instruments',
            'Wave Optics: Interference and Diffraction',
            'Polarization',
            'Dispersion and Spectra',
            'Optical Phenomena in Nature',
        ],
        'Modern Physics': [
            'Quantum Physics and Quantum Mechanics',
            'Dual Nature of Matter and Radiation',
            'Atomic and Nuclear Physics',
            'Special and General Relativity',
            'Particle Physics and Standard Model',
            'Cosmology and Universe',
        ],
        'Fluid Mechanics': [
            'Fluid Properties and Statics',
            'Fluid Dynamics and Bernoulli\'s Principle',
            'Viscosity and Laminar Flow',
            'Surface Tension and Capillarity',
            'Turbulence and Flow Patterns',
        ],
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
