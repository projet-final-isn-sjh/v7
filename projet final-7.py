import tkinter as tk
from math import cos,sin,sqrt,pi

class Display(tk.Frame):
    #Classe qui gère l'affichage à l'écran
    def __init__(self,parent,data,step):
        tk.Frame.__init__(self,parent)
        self.parent=parent
        self.step=step
        self.canvas=tk.Canvas(self.parent,width=800,height=450,bg='blue')
        self.canvas.pack()
        self.canvas.create_polygon(185,370,215,370,215,400,185,400,fill="red",outline="pink",width=5,tag="cube")
        self.canvas.create_rectangle(0,400,800,450,fill="grey",width=3,outline="white")
        self.canvas.create_text(400,430,tag="text",font=("Arial","25"),fill="white")
        self.counter=0
        self.lenght_jmp=25
        self.shapes=([0,450],
                     [0,0,40,0,40,40,0,40],
                     [0,40,20,6,40,40])
        self.data=self.decode(data)
        self.lenght=len(self.data)-1
        self.r=sqrt(2)*15

    def create_object(self,shape_property):
        shape,height,x=shape_property
        points=self.shapes[shape]
        m=(len(points))//2
        x=[points[2*i]+x for i in range(m)]
        y=[height+points[2*i+1] for i in range(m)]
        points=[(x[i],y[i]) for i in range(m)]
        self.canvas.create_polygon(points,fill="purple",outline="white",width=2,tags=("h"+str(height),"s"+str(shape),"map","c"+str(self.counter)))

    def move(self):
        self.canvas.move("map",self.step,0)
        instruction=self.data[self.counter]
        self.create_object(instruction)
        self.canvas.delete("c"+str(self.counter-185))
        self.counter+=1
        self.canvas.itemconfig("text",text=percent(self.counter,self.lenght))

    def Point(self,x,y):
        tag=self.canvas.gettags(max((1,)+self.canvas.find_overlapping(x,y,x,y)))
        if len(tag)==4:
            return int(tag[0][1:]),int(tag[1][1:])
        else:
            return 0,0

    def pc(self,r,t,xo=200,yo=400):
        return xo+int(r*cos(t)),yo+int(r*sin(t))

    def cube(self,y,m):
        t=pi/(2*self.lenght_jmp)*m
        coords=self.pc(self.r,t+3*pi/4,yo=y)+self.pc(self.r,t+pi/4,yo=y)+self.pc(self.r,t-pi/4,yo=y)+self.pc(self.r,t-3*pi/4,yo=y)
        self.canvas.coords("cube",coords)

    def Get_Sensor(self,x,y):
        return [self.Point(x-15,y),self.Point(x+15,y),self.Point(x+15,y-30),self.Point(x-15,y-30)]
    
    def decode(self,data):
        texture=list()
        lines=data.split("\n")
        for line in lines:
            instructions=line.split("+")
            l=len(instructions)
            for i in range(l):
                instruction=instructions[i].split("-")
                texture.append((int(instruction[0]),int(instruction[1]),760+i*self.step))
            for i in range(10-l):
                texture.append((0,0,760+(l+i)*self.step))
        return texture


class Movement(Display):

    def __init__(self):
        #Effacer tous les éléments de la fenêtre
        clean(root)
        #Variables
        self.vy=0
        self.y=200
        self.stop=False
        self.jmp=False
        self.last_jmp=0
        self.disable_jmp=True
    
        #Cette classe hérite de la classe Display
        Display.__init__(self,root,data,-4)
        Display.pack(self,side="top", fill="both", expand=True)
        root.bind("<space>",self.jump)
        #initialisation du mouvement
        self.append()
 
    def append(self):
        self.sensor=Display.Get_Sensor(self,200,self.y)
        #Sol
        sol=self.y>=400
        self.bottom_sensor=(1-sol)*max(self.sensor[0][0],self.sensor[1][0])+sol*400           
        
        self.y-=int((3/5)*self.vy)
        self.vy-=1

        if self.bottom_sensor:
            self.y=self.bottom_sensor
            self.vy=0

            if self.jmp:
                self.jmp=False
                self.last_jmp=self.counter
                self.vy=20
                self.y-=5
                
        self.disable_jmp=(self.counter-self.last_jmp)*(self.counter-self.last_jmp<self.lenght_jmp)
        self.life_sensor=(self.sensor[1][1],self.sensor[2][1])
        
        if self.life_sensor==(1,1):
            self.stop=True        

        #Display    
        Display.move(self)
        Display.cube(self,self.y-19,self.disable_jmp)
        
        if self.counter!=self.lenght and not self.stop:
            root.after(13,self.append)
        if self.stop==True:
            Score(root,self.counter,self.lenght)


            
    def jump(self,event):
        #Si on se trouve au delà du milieu du saut, alors le saut est autorisé
        if not self.disable_jmp:
            self.jmp=True

    
class Score(tk.Frame):
    def __init__(self,parent,counter,lenght):
        clean(root)
        tk.Frame.__init__(self,parent)
        self.parent=parent
        score=percent(counter,lenght)
        tk.Label(self.parent,text=score).pack()
        tk.Button(self.parent,text="Retry",command=Movement).pack()


def clean(parent):
    for i in parent.winfo_children():
        i.destroy()

def percent(counter,lenght):
    return str(int(counter/lenght*100))+"%"

        
file=open("map.txt","r")
data=file.read()
file.close()


root=tk.Tk()
root.title("Geometry Dash")
root.resizable(False,False)

m=Movement()
root.mainloop()

