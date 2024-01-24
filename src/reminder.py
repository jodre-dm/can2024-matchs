def main():
    initial_times = ["00:00", "15:00", "18:00", "21:00"]
    for initial_time in initial_times:
        cinq_minutes = reminder_time(initial_time, 0, 5)
        dix_minutes = reminder_time(initial_time, 0, 10)
        trente_minutes = reminder_time(initial_time, 0, 30)
        une_heure  = reminder_time(initial_time, 1, 0)
        h24 = reminder_time(initial_time, 24, 0)

        print(f"Heure initiale {initial_time}\n \
              - moins {5} minutes   : {cinq_minutes}\n \
              - moins {10} minutes  : {dix_minutes}\n \
              - moins {30} minutes  : {trente_minutes}\n \
              - moins {1} heure     : {une_heure}\n \
              - moins {24} heures   : {h24}\n"
              )




if __name__ == "__main__":
    main()