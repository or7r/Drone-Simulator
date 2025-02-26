from Objects.Drone import Drone
from Objects.Path import Path
from Objects.Enums.ForceSide import FroceSide
from blue_forces_coverage import create_blue_forces_coverage_gaza
from time import sleep
def main():
    path_Gaza_Short_Routes = [[(31.3443293, 34.3095897), (31.2456487, 34.8577683)],
                               [(31.557994, 34.9762809), (31.8952532, 34.8105616)]]
    path_Gaza_Long_Routes = [[(31.557994, 34.9762809), (31.9635712, 34.8101149)],
                            [(31.5128679, 34.4581358), (32.2848603, 34.9801701)],
                            [(31.2752047, 34.2558269), (31.9324487, 35.0433428)],
                            [(31.2752047, 34.2558269), (32.994254, 35.309878)],
                            [(31.557994, 34.9762809), (32.8502229, 35.0703245)],
                            [(31.557994, 34.9762809), (32.2848603, 34.9801701)],
                            [(31.54977, 34.5024697), (32.0500659, 34.9521522)]]
    path_Beirut_Rostart_coordinateutes = [[(33.22435219349651, 35.24215575703209), (32.9159104, 35.293429)],
                           [(33.595839412403194, 35.93307769262191), (31.7788242, 35.2257626)],
                           [(33.449715313317476, 35.53353807828087), (32.0193121, 34.7804076)],
                           [(33.920018951001246, 35.15937093875041), (32.0604256, 34.8760954)],
                           [(33.572998707073396, 35.60439645493808), (32.8502229, 35.0703245)],
                           [(33.075386612825454, 35.89551071585173), (32.0852997, 34.7818064)],
                           [(33.59121684110817, 35.75435880712383), (32.2848603, 34.9801701)],
                           [(33.32775683934265, 35.907261006337365), (32.8115853, 35.1163747)],
                           [(33.89507729660031, 35.59950974811788), (31.150071, 34.983628)]]
    path_Inside_Israel_Routes = [[(32.3286181, 34.8566246), (32.9548871, 35.2087895)],
                                 [(32.8114088, 35.259756), (32.0604256, 34.8760954)],
                                 [(32.1860244, 34.8678359), (32.5029914, 35.0504995)],
                                 [(32.5202891, 34.9435862), (32.0331756, 34.8907527)],
                                 [(32.6922393, 35.0482785), (31.779277712233252, 35.21091595846688)],
                                 [(32.9159104, 35.293429), (32.8869441, 35.406944)],
                                 [(31.6070652, 34.76985308061673), (32.0154565, 34.7505283)],
                                 [(32.1060817, 35.1851368), (32.994254, 35.309878)],
                                 [(32.723612, 35.312492), (32.8285812, 35.0844915)]]
    drones = []
    radars = create_blue_forces_coverage_gaza()
    for i in range(len(path_Inside_Israel_Routes)):
        drones.append(Drone(1, 30, FroceSide.BLUE, Path(path_Inside_Israel_Routes[i][0], path_Inside_Israel_Routes[i][1])))
    
    all_data = []

    for d in drones:
        # sleep(1)
        d.update_state()
    

    while any([d.is_flying_func() for d in drones]):
        is_visible = True #any([r.is_coordinate_visible(d.get_current_location()) for r in radars])
        print(is_visible)
        if is_visible:
            
            drone_update = [d.get_id(), d.force_side.name, d.current_flight.get_time(), 
                            float(d.current_location[0]), float(d.current_location[1]), d.get_current_speed(),
                            d.current_flight.get_id()]
            all_data.append(drone_update)
            print(drone_update)
            print(str(d))

        if len(all_data) >= 40:
            import pandas as pd
            df = pd.DataFrame(all_data, columns=["drone_id", "force_side_name", "time", 
                                                    "lat", "lon", "speed", "flight_id"])
            df.to_csv("data.csv")
            import sys
            sys.exit()

    print("finished")           
        
if __name__ == "__main__":
    main()