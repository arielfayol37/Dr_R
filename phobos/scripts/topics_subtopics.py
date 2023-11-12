from phobos.models import Topic, SubTopic, Subject, Unit

def run():
    
    subjects = ['PHYSICS']
    # Define a dictionary with topics, subtopics, and units
    topics_subtopics_units_list = [
            {
                'Mechanics': {
                    'Kinematics': [
                        'Motion in One Dimension',
                        'Motion in Two Dimensions',
                        'Projectile Motion',
                        'Uniform Circular Motion',
                    ],
                    'Newton\'s Laws of Motion': [
                        'Force and Inertia',
                        'Applications of Newton\'s Laws',
                        'Frictional Forces',
                        'Non-inertial Frames and Pseudo Forces',
                    ],
                    'Work, Energy, and Power': [
                        'Work Done by a Constant Force',
                        'Work Done by a Variable Force',
                        'Kinetic and Potential Energy',
                        'Conservation of Energy',
                        'Power',
                    ],
                    'Momentum and Collisions': [
                        'Linear Momentum and Impulse',
                        'Conservation of Linear Momentum',
                        'Collisions in One Dimension',
                        'Collisions in Two Dimensions',
                        'Center of Mass',
                    ],
                    'Circular and Rotational Motion': [
                        'Rotational Kinematics',
                        'Rotational Dynamics',
                        'Angular Momentum and Its Conservation',
                        'Gyroscopic Effects',
                    ],
                    'Gravitation': [
                        'Newton\'s Law of Universal Gravitation',
                        'Gravitational Potential Energy',
                        'Orbits of Planets and Satellites',
                        'Gravitational Fields',
                    ],
                    'Statics of Rigid Bodies': [
                        'Equilibrium of Rigid Bodies',
                        'Statics of Structures',
                        'Centroids and Centers of Gravity',
                        'Stress and Strain',
                    ],
                    'Dynamics of Rigid Bodies': [
                        'Torque and Angular Acceleration',
                        'Rotational Work and Energy',
                        'Rotational Collisions',
                        'Dynamics of Rotational Motion',
                    ],
                },
                'Thermodynamics': {
                    'Thermal Properties of Matter': [
                        'Temperature and Heat',
                        'Thermal Expansion',
                        'Heat Capacity',
                        'Phase Transitions',
                    ],
                    'Thermal Equilibrium and Temperature': [
                        'Zeroth Law of Thermodynamics',
                        'Thermometers and Temperature Scales',
                        'Thermal Contact and Equilibrium',
                    ],
                    'First Law of Thermodynamics': [
                        'Internal Energy',
                        'Heat and Work',
                        'Thermodynamic Processes',
                    ],
                    'Second Law of Thermodynamics': [
                        'Heat Engines',
                        'Refrigerators and Heat Pumps',
                        'Entropy',
                        'Carnot Cycle',
                    ],
                    'Heat Transfer Methods': [
                        'Conduction',
                        'Convection',
                        'Radiation',
                    ],
                    'Thermodynamic Processes': [
                        'Isothermal Process',
                        'Adiabatic Process',
                        'Isobaric Process',
                        'Isochoric Process',
                    ],
                    'Entropy and Carnot Cycle': [
                        'Statistical Interpretation of Entropy',
                        'Entropy Changes and Processes',
                        'The Carnot Engine',
                        'Efficiency of Heat Engines',
                    ],
                    'Heat Engines and Refrigerators': [
                        'Otto Cycle',
                        'Diesel Cycle',
                        'Refrigeration Cycles',
                    ],
                },

                'Electricity and Magnetism': {
                    'Electrostatics': [
                        'Charge and Coulomb\'s Law',
                        'Electric Field',
                        'Electric Potential',
                        'Capacitors and Dielectrics',
                    ],
                    'Electric Potential and Capacitance': [
                        'Potential Energy in Electric Fields',
                        'Equipotential Surfaces',
                        'Capacitance',
                        'Energy Stored in Capacitors',
                    ],
                    'Current Electricity': [
                        'Electric Current and Drift Speed',
                        'Resistance and Ohm\'s Law',
                        'Electrical Power',
                        'Direct and Alternating Current Circuits',
                    ],
                    'Magnetic Effects of Current': [
                        'Magnetic Fields and Forces',
                        'Biot-Savart Law',
                        'Ampère\'s Law',
                        'Electromagnetic Induction',
                    ],
                    'Electromagnetic Induction and AC': [
                        'Faraday\'s Law',
                        'Lenz\'s Law',
                        'AC Generators',
                        'Transformers',
                    ],
                    'Electromagnetic Waves': [
                        'Wave Equation',
                        'Energy in Electromagnetic Waves',
                        'Propagation of Electromagnetic Waves',
                        'Polarization of Light',
                    ],
                    'Maxwell\'s Equations': [
                        'Gauss\'s Law for Electricity',
                        'Gauss\'s Law for Magnetism',
                        'Faraday\'s Law of Induction',
                        'Ampère-Maxwell Law',
                    ],
                },

                'Waves': {
                    'Wave Basics and Types': [
                        'Transverse and Longitudinal Waves',
                        'Wave Parameters and Equations',
                        'Wave Speed on a String',
                    ],
                    'Wave Properties and Behavior': [
                        'Reflection and Refraction of Waves',
                        'Interference and Diffraction',
                        'Standing Waves and Resonance',
                    ],
                    'Superposition and Standing Waves': [
                        'Principle of Superposition',
                        'Formation of Standing Waves',
                        'Harmonics and Overtones',
                    ],
                    'Sound Waves': [
                        'Characteristics of Sound',
                        'The Doppler Effect',
                        'Acoustics',
                        'Ultrasound and Applications',
                    ],
                    'Doppler Effect': [
                        'Doppler Shift for Sound Waves',
                        'Doppler Shift for Light Waves',
                        'Applications in Astronomy and Radar',
                    ],
                    'Resonance': [
                        'Resonance in Strings and Air Columns',
                        'Electrical Resonance in Circuits',
                        'Resonance in Buildings and Bridges',
                    ],
                },
                'Optics': {
                    'Reflection and Refraction': [
                        'Laws of Reflection',
                        'Snell\'s Law',
                        'Total Internal Reflection',
                        'Fiber Optics',
                    ],
                    'Lens, Mirrors, and Optical Instruments': [
                        'Converging and Diverging Lenses',
                        'Mirror Equations',
                        'Microscopes and Telescopes',
                        'Camera and Optical Sensors',
                    ],
                    'Wave Optics: Interference and Diffraction': [
                        'Young\'s Double-Slit Experiment',
                        'Diffraction Grating',
                        'X-ray Diffraction',
                        'Holography',
                    ],
                    'Polarization': [
                        'Polarization by Reflection',
                        'Polarization by Scattering',
                        'Liquid Crystal Displays',
                        'Optical Activity in Materials',
                    ],
                    'Dispersion and Spectra': [
                        'Prism and Rainbows',
                        'Spectral Lines and Emission Spectra',
                        'Absorption Spectra',
                        'Spectroscopy',
                    ],
                    'Optical Phenomena in Nature': [
                        'Mirages',
                        'Rainbows',
                        'Auroras',
                        'The Blue Sky and Sunset',
                    ],
                },
                'Modern Physics': {
                    'Quantum Physics and Quantum Mechanics': [
                        'Photoelectric Effect',
                        'Wave-Particle Duality',
                        'Quantum Tunneling',
                        'Quantum Entanglement',
                    ],
                    'Dual Nature of Matter and Radiation': [
                        'De Broglie Hypothesis',
                        'Davisson-Germer Experiment',
                        'Compton Scattering',
                    ],
                    'Atomic and Nuclear Physics': [
                        'Rutherford\'s Atomic Model',
                        'Nuclear Reactions',
                        'Radioactivity',
                        'Nuclear Fission and Fusion',
                    ],
                    'Special and General Relativity': [
                        'Time Dilation and Length Contraction',
                        'Mass-Energy Equivalence',
                        'Gravitational Time Dilation',
                        'Black Holes and Event Horizons',
                    ],
                    'Particle Physics and Standard Model': [
                        'Elementary Particles',
                        'Forces and Mediator Particles',
                        'Accelerators and Detectors',
                        'Quarks and Leptons',
                    ],
                    'Cosmology and Universe': [
                        'Big Bang Theory',
                        'Cosmic Microwave Background',
                        'Dark Matter and Dark Energy',
                        'Expansion of the Universe',
                    ],
                },
                'Fluid Mechanics': {
                    'Fluid Properties and Statics': [
                        'Density and Pressure',
                        'Buoyancy and Archimedes\' Principle',
                        'Fluids in Motion',
                        'Bernoulli\'s Equation',
                    ],
                    'Fluid Dynamics and Bernoulli\'s Principle': [
                        'Streamline Flow and Turbulence',
                        'Viscosity and Reynolds Number',
                        'Flow Rate and Continuity Equation',
                        'Applications of Bernoulli\'s Principle',
                    ],
                    'Viscosity and Laminar Flow': [
                        'Viscous Forces and Poiseuille\'s Law',
                        'Flow in Pipes and Channels',
                        'Stokes\' Law and Terminal Velocity',
                    ],
                    'Surface Tension and Capillarity': [
                        'Cohesion and Adhesion',
                        'Drops and Bubbles',
                        'Capillary Action',
                        'Detergents and Surfactants',
                    ],
                    'Turbulence and Flow Patterns': [
                        'Characterization of Turbulent Flow',
                        'Vortices and Eddies',
                        'Aerodynamics and Hydrodynamics',
                        'Flow Measurement Techniques',
                    ],
                },
            },
    ]
    for index, topics_subtopics_units in enumerate(topics_subtopics_units_list):
        subject, created = Subject.objects.get_or_create(name=subjects[index])
        # Create instances of subtopics using nested for loops and the dictionary values
        for topic_name, subtopics_units_dict in topics_subtopics_units.items():
            # Check if the topic already exists in the database
            topic, created = Topic.objects.get_or_create(name=topic_name, subject=subject)
            
            # If the topic was just created, print a message
            if created:
                print(f"Created new topic: {topic_name}")
            
            for subtopic_name in subtopics_units_dict:
                st, created = SubTopic.objects.get_or_create(topic=topic, name=subtopic_name)

                for unit_name in subtopics_units_dict[subtopic_name]:
                    unit, created = Unit.objects.get_or_create(name=unit_name, subtopic=st)

    # Verify the creation of objects
    print(Topic.objects.all())
    print(SubTopic.objects.all())
    print(Unit.objects.all())


