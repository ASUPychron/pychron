'''
modifier: 01
'''
def main():
    info("Jan Cocktail Pipette x1")
    gosub('jan:WaitForMiniboneAccess')
    gosub('jan:PrepareForAirShot')
    gosub('jan:EvacPipette1')
    gosub('common:FillPipette1')
    gosub('jan:PrepareForAirShotExpansion')
    gosub('common:SniffPipette1')
    