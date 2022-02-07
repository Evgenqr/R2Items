
def monster_list():
    queryset = Monster.objects.all()
    monsters = []
    for monster in queryset:
        monsters.append({'id': monster.id, 'name': monster.name})
    return monsters


monster_list()
