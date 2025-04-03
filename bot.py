# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from tilthenightends import Levelup, LevelupOptions, Vector, Team, Towards


RNG = np.random.default_rng(seed=12)


class Leader:
    def __init__(self, hero: str):
        self.hero = hero
        self.next_turn = 2.5
        self.vector = Vector(1, 1)

    def run(self, t, dt, monsters, players, pickups) -> Vector | Towards | None:
        me = players[self.hero]
        if t > self.next_turn:
            self.vector = Vector(*RNG.random(2) * 2 - 1)
            self.next_turn += 5.0
            if len(monsters) > 0:
                lavdist = 0.; nm = 0
                mdist = 6e5
                m = {'x':[], 'y':[], 'health':[], 'attack':[]}
                for mm in monsters.values():
                    for x in mm.x: m['x'].append(x)
                    for y in mm.y: m['y'].append(y)
                    for h in mm.healths: m['health'].append(h)
                    for a in mm.attacks: m['attack'].append(a)
                m['x'] = np.array(m['x'])
                m['y'] = np.array(m['y'])
                m['health'] = np.array(m['health'])
                m['attack'] = np.array(m['attack'])
                fx = 0.
                fy = 0.
                for i in range(len(m['x'])):
                    vx = me.x - m['x'][i]
                    vy = me.y - m['y'][i]
                    dist = np.sqrt(vx**2 + vy**2)
                    q = m['health'][i] + m['attack'][i]
                    fx += q / dist**2 * vx / dist
                    fy += q / dist**2 * vy / dist
                
                ff = np.sqrt(fx**2 + fy**2)
                if ff > 0:
                    fx /= ff
                    fy /= ff
                
                return Vector(fx+0.3,fy+0.3)

        return self.vector


class Follower:
    def __init__(self, hero: str, following: str):
        self.hero = hero
        self.following = following

    def run(self, t, dt, monsters, players, pickups) -> Vector | Towards | None:
        for name, player in players.items():
            if name == self.following:
                return Towards(player.x, player.y)
        return None


class Brain:
    def __init__(self):
        pass

    def levelup(self, t: float, info: dict, players: dict) -> Levelup:
        if np.random.uniform() < 0.6:
            return Levelup("garron", LevelupOptions.weapon_damage)
        # A very random choice
        for hero in players.keys():
            if players[hero].alive:
                if players[hero].health < 0.3 * players[hero].max_health:
                    return Levelup(hero, LevelupOptions.player_health)
        lowest_speed = 1e6
        hcool = 0
        for hero in players.keys():
            #if players[hero].alive and players[hero].speed < lowest_speed:
            if players[hero].alive and players[hero].weapon.cooldown > hcool:
                hcool = players[hero].weapon.cooldown
                chero = hero
        return Levelup(chero, LevelupOptions.weapon_cooldown)
        #return Levelup(chero, LevelupOptions.player_speed)
        hero = RNG.choice(list(players.keys()))
        what = RNG.choice(list(LevelupOptions))
        return Levelup(hero, what)


#    players=[
#        Leader(hero="alaric"),
#        Follower(hero="kaelen", following="alaric"),
#        Follower(hero="garron", following="alaric"),
#        Follower(hero="isolde", following="alaric"),
#        Follower(hero="lyra", following="alaric"),
#    ],
team = Team(
    players=[
        Leader(hero="seraphina"),
        Follower(hero="kaelen", following="seraphina"),
        Follower(hero="evelyn", following="seraphina"),
        Follower(hero="garron", following="seraphina"),
        Follower(hero="theron", following="seraphina"),
        #Follower(hero="alaric", following="isolde"),
        #Follower(hero="cedric", following="seraphina"),
    ],
    strategist=Brain(),
)
