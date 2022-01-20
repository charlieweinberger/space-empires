from ships import *

scout         = {'name': 'Scout',         'hp': 1, 'atk': 3, 'df': 0, 'ship_class': 'E', 'cp_cost': 6,  'maint_cost': 1}
destroyer     = {'name': 'Destroyer',     'hp': 1, 'atk': 4, 'df': 0, 'ship_class': 'D', 'cp_cost': 9,  'maint_cost': 1}
cruiser       = {'name': 'Cruiser',       'hp': 2, 'atk': 4, 'df': 1, 'ship_class': 'C', 'cp_cost': 12, 'maint_cost': 2}
battlecruiser = {'name': 'BattleCruiser', 'hp': 2, 'atk': 5, 'df': 1, 'ship_class': 'B', 'cp_cost': 15, 'maint_cost': 2}
battleship    = {'name': 'Battleship',    'hp': 3, 'atk': 5, 'df': 2, 'ship_class': 'A', 'cp_cost': 20, 'maint_cost': 3}
dreadnaught   = {'name': 'Dreadnaught',   'hp': 3, 'atk': 6, 'df': 3, 'ship_class': 'A', 'cp_cost': 24, 'maint_cost': 3}

all_ships = [scout, destroyer, cruiser, battlecruiser, battleship, dreadnaught]
ship_objects = {
    'Scout': Scout,
    'Destroyer': Destroyer,
    'Cruiser': Cruiser,
    'BattleCruiser': BattleCruiser,
    'Battleship': Battleship,
    'Dreadnaught': Dreadnaught
}

  def complete_economic_phase(self):
    
    self.logs.write('\nBEGINNING OF TURN {} ECONOMIC PHASE\n'.format(self.turn))
    
    for player in self.players:
      
      player.cp += 10
      
      self.maintenance(player)

      player_ships = player.buy_ships(player.cp)
      total_cost = self.calc_total_cost(player_ships)
      
      if total_cost > player.cp:
        self.logs.write('\n\tPlayer {} went over budget'.format(player.player_num))
        continue
      
      player.cp -= total_cost
      self.logs.write('\n\tPlayer {} buys the following ships:'.format(player.player_num))
      
      for name in player_ships:
        for i in range(player_ships[name]):
          init_coords = player.home_colony.coords
          ship = ship_objects[name](init_coords)
          if ship == None:
            continue
          player.add_ship(ship)
          self.logs.write('\n\t\t Player {} {} {}'.format(ship.player_num, ship.name, ship.ship_num))
        self.logs.write('\n')

    self.logs.write('\nEND OF TURN {} ECONOMIC PHASE\n'.format(self.turn))