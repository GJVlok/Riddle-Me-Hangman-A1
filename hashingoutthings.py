from actors import actors_dict

songs = set(actors_dict)

my_dict = {item: 'Actors' for item in songs}
print(len(my_dict))