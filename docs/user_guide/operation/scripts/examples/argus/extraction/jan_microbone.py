'''
modifier: 01
eqtime: 12 
'''
def main():
    info('Jan microbone blank analysis')

    if analysis_type=='blank':
        info('is blank. not heating')
        
        close(name="L", description="Microbone to Minibone")
        close(name="A", description="CO2 Laser to Jan")
        open(name="T", description="Microbone to CO2 Laser")
        close(name="K", description="Microbone to Getter NP-10C")
        close(name="M", description="Microbone to Getter NP-10H")
        open(name="S", description="Microbone to Inlet Pipette")
        sleep(duration=30.0)
        close(description='Microbone to Turbo')
        
        sleep(duration)
        sleep(cleanup)



    
