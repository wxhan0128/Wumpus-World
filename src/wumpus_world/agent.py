import copy

class Agent:
    infer_wumpus = set()
    sure_wumpus = set()
    wumpus_coord = set()

    infer_pits = set()
    sure_pits = set()
    pit_coord = set()
        
    safe_place = set()
    
    cur_loc = []
    up = []
    down = []
    left = []
    right = []
    
    track = []
    
    def get_action(self):
        move_actions = []
        extras_actions = []
        
        move_actions = self.prepare_move()
        
        state = self.killed_wumpus()
        print('killed?', state)
        
        if move_actions:
            if state == 0:  # have not find wumpus
                from random import choice
                return choice(move_actions)

            elif state == 1:  # have found and prepare to shoot
                extras_actions = self.prepare_shoot_wumpus()
                print('shoot?', extras_actions)
                if extras_actions:
                    for i in self.sure_wumpus:
                        self.safe_place.add(i)
                    self.sure_wumpus.clear()
                    
                    for j in self.sure_pits:
                        self.safe_place.remove(j)
                        
                    return extras_actions[0]
                else:
                    from random import choice
                    return choice(move_actions)
                
            elif state == 2:  # the wumpus died
                from random import choice
                return choice(move_actions)
        else:
            return 'QUIT'
            
    def give_senses(self, location, breeze, stench):
        self.cur_loc = location
        dir_list = []
        self.safe_place.add(location)
            
        self.up = (location[0] , location[1] + 1)
        self.down = (location[0], location[1] - 1)
        self.left = (location[0] - 1, location[1])
        self.right = (location[0] + 1, location[1])
        dir_list.append(self.up)
        dir_list.append(self.down)
        dir_list.append(self.left)
        dir_list.append(self.right)
        
        if self.track:
            if location != self.track[len(self.track) - 1] and location not in self.track:
                if not breeze and not stench :
                    self.refresh_safeKB(dir_list)
                    print('safe place', self.safe_place)
                    print('maybe wumpus', self.infer_wumpus)
                    print('sured wumpus', self.sure_wumpus)
            
                elif stench and not breeze:
                    state = self.killed_wumpus()
                    if state != 2:
                        self.refresh_wumpusKB(dir_list)
                    print('safe place', self.safe_place)
                    print('maybe wumpus', self.infer_wumpus)
                    print('sured wumpus', self.sure_wumpus)
            
                elif breeze and not stench:
                    self.refresh_pitsKB(dir_list)
                    print('safe place', self.safe_place)
                    print('maybe pit', self.infer_pits)
                    print('sured pit', self.sure_pits)
                
                elif breeze and stench:
                    state = self.killed_wumpus()
                    self.refresh_pitsKB(dir_list)
                    if state != 2:
                        self.refresh_wumpusKB(dir_list)
                    print('safe place', self.safe_place)
                    print('maybe wumpus', self.infer_wumpus)
                    print('sured wumpus', self.sure_wumpus)
                    print('maybe pit', self.infer_pits)
                    print('sured pit', self.sure_pits)
                    
        # do with the first step
        else:
            if not breeze and not stench :
                self.refresh_safeKB(dir_list)
            else:
                return 'QUIT'

        self.track.append(location)
    
    def refresh_safeKB(self, movelist):
        for i in movelist:
            self.safe_place.add(i)
            if i in self.infer_wumpus:
                self.infer_wumpus.remove(i)
            if i in self.infer_pits:
                self.infer_pits.remove(i)
                
    def refresh_wumpusKB(self, movelist):
        for i in movelist:
            if i not in self.sure_wumpus and i not in self.safe_place:
                if i in self.infer_wumpus:
                    self.sure_wumpus.add(i)
                    self.infer_wumpus.remove(i)
                else:
                    self.infer_wumpus.add(i)
        
        if self.sure_wumpus:
            for i in self.infer_wumpus:
                if i not in self.infer_pits:
                    self.safe_place.add(i)
            self.infer_wumpus.clear()
    
    def refresh_pitsKB(self, movelist):
        print('find a pit', self.sure_pits)
                    
        if self.sure_pits:
            for i in self.infer_pits:
                if i in self.track:
                    self.safe_place.add(i)
            self.infer_pits.clear()
        else:
            for i in movelist:
                if i not in self.sure_pits and i not in self.safe_place:
                    if i in self.infer_pits:
                        self.sure_pits.add(i)
                        self.infer_pits.remove(i)
                    else:
                        self.infer_pits.add(i)
    
    def prepare_move(self):
        p = []
        q = []
        
        if self.up in self.safe_place:
            p.append(self.up)
        if self.down in self.safe_place:
            p.append(self.down)
        if self.left in self.safe_place:
            p.append(self.left)
        if self.right in self.safe_place:
            p.append(self.right)
        
        print('the available steps ', p)
            
        if self.up in p:
            q.append('MOVE_UP')
        if self.down in p:
            q.append('MOVE_DOWN')
        if self.right in p:
            q.append('MOVE_RIGHT')
        if self.left in p:
            q.append('MOVE_LEFT')
        
        return q
        
    def prepare_shoot_wumpus(self):
        p = []
        if self.sure_wumpus:
            for i in self.sure_wumpus:
                if i[0] == self.cur_loc[0] and i[1] > self.cur_loc[1]:
                    p.append('SHOOT_UP')
                if i[0] == self.cur_loc[0] and i[1] < self.cur_loc[1]:
                    p.append('SHOOT_DOWN')
                if i[0] < self.cur_loc[0] and i[1] == self.cur_loc[1]:
                    p.append('SHOOT_LEFT')      
                if i[0] > self.cur_loc[0] and i[1] == self.cur_loc[1]:
                    p.append('SHOOT_RIGHT')
        
        return p
                               
    def killed_wumpus(self):
        findandkill = 0
        
        if self.sure_wumpus:
            self.wumpus_coord = copy.deepcopy(self.sure_wumpus)
        
        print('find a wumpus', self.wumpus_coord)
        
        # has killed
        if self.wumpus_coord and self.wumpus_coord <= self.safe_place:
            findandkill = 2
        
        # did not find
        elif not self.wumpus_coord and not (self.wumpus_coord <= self.safe_place):
            findandkill = 0
        
        # just find and did not kill
        elif self.wumpus_coord and not (self.wumpus_coord <= self.safe_place):
            findandkill = 1
            
        return findandkill
             
a = Agent()
