from project_app.models import User, Course, Section, Role


supervisor = User(username='supervisor', email='supervisor@uwm.edu',
                  first_name='Test', last_name='Supervisor')
supervisor.set_password('supervisor')
supervisor.role = Role.SUPERVISOR
supervisor.save()

rock = User(username='rock', email='rock@uwm.edu',
            first_name='Jayson', last_name='Rock')
rock.set_password('rock')
rock.role = Role.INSTRUCTOR
rock.save()

apasad = User(username='aprasad', email='aprasad@uwm.edu',
              first_name='Apoorv', last_name='Prasad')
apasad.set_password('aprasad')
apasad.role = Role.TA
apasad.save()

software_engineering = Course(name='Introduction to Software Engineering',
                              subject='COMPSCI', number='361', instructor=rock)
software_engineering.save()

rock.courses.add(software_engineering)
rock.save()

apasad.courses.add(software_engineering)
apasad.save()

section = Section(number='891', course=software_engineering)
section.save()

section.tas.add(apasad)

discrete_information_structures = Course(
    name='Discrete Information Structure', subject='COMPSCI', number='317', instructor=rock)
discrete_information_structures.save()

rock.courses.add(discrete_information_structures)
rock.save()
