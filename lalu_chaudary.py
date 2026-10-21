# World Simulation...
import csv
import statistics
import random

world_width = 20
world_height = 10
world_population = 8
initial_food = 24
food_per_turn = 4
max_turns = 100

starting_energy =  18
max_energy = 54
reproduction_energy = 25
reproduction_cost =  7
mutation_chance = 0.23

class Chij:
    def __init__(self, x, y, speed = 1, efficiency = 1.0, energy = starting_energy, genaration = 0):
        self.x = x
        self.y = y
        self.speed = speed
        self.efficiency = efficiency
        self.energy = energy
        self.age = 0
        self.generation = genaration

    def move(self):
        for _ in range(self.speed):
            direction = random.choice(["up", "down", "left", "right"])

            if direction == "up":
                self.y = self.y - 1
            elif direction == "down":
                self.y = self.y + 1
            elif direction == "left":
                self.x = self.x -1
            else:
                self.x = self.x + 1

        self.x = max(0,min(world_width - 1, self.x))
        self.y = max(0,min(world_width - 1, self.y))

        self.energy = self.energy -(1.0/self.efficiency)
        if self.energy <= 0:
            exit

    def eat(self, food):
        if(self.x, self.y) in food:
            food.remove((self.x,self.y))
            self.energy = min(max_energy, self.energy + random.randint(1, 10))
            return True
        return False

    def is_alive(self):
        if self.energy <= 0:
            return False
        if self.age <=50:
            death_chance =  0.04
        else:
            death_chance = 0.30

        return random.random() >= death_chance
    
def create_food(number):
        food= set()

        while len(food) < number:
            x = random.randint(0, world_width - 1)
            y = random.randint(0, world_height - 1)
            food.add((x,y))
        return food

def reproduce(parent):
        child_speed = parent.speed
        child_efficiency = parent.efficiency

        if random.random() < mutation_chance:
            child_speed += random.choice([1, -1, -2, 2])
            child_speed = max(1,min(10,child_speed))

        if random.random() < mutation_chance:
            child_efficiency += random.uniform(-0.5, 0.5)
            child_efficiency = max(0.2, min(5.0,child_efficiency))
            child_efficiency = round(child_efficiency, 1)
        child = Chij(
            x = parent.x,
            y = parent.y,
            speed = child_speed,
            efficiency = child_efficiency,
            energy = reproduction_cost,
            genaration = parent.generation + 1
        )

        parent.energy = parent.energy - reproduction_cost
        return child

def world_pov(chij, food, turn):
        print("\n" + "=" *50)
        print(f"TURN{turn}")
        print("\n"*50)

        chij_position = {(c.x,c.y) for c in chij}

        for y in range(world_height):
            row = " "
            for x in range (world_width):
                if (x,y) in chij_position:
                    row += "O "
                elif(x,y) in food:
                    row += "F "
                else:
                    row +=". "
            print(row)

        if chij:
            avg_energy = sum(c.energy for c in chij) / len(chij)
            avg_speed  = sum(c.speed for c in chij ) / len(chij)
            avg_efficiency = sum(c.efficiency for c in chij) / len(chij)
            highest_generation = max(c.generation for c in chij)

            print(f"\nPopulation: {len(chij)}")
            print(f"Food remaining: {len(food)}")
            print(f"Average energy: {avg_energy:.1f}")
            print(f"Average speed: {avg_speed:.2f}")
            print(f"Average efficiency: {avg_efficiency:.2f}")
            print(f"Highest generation alive: {highest_generation}")
        else:
             print("\nPopulation: 0")
             print("All organisms have died out.")

def main():
       
    chij = []

    for _ in range(world_population):
        x = random.randint(0, world_width - 1)
        y = random.randint(0, world_height - 1)
        speed = random.randint(1, 2)
        efficiency = random.choice([0.8, 1.0, 1.2])

        chij.append(
            Chij(x, y, speed=speed, efficiency=efficiency)
        )

    food = create_food(initial_food)
    highest_generation = 0
    turns_completed = 0

    for turn in range(1, max_turns + 1):
        if not chij:
            break

        food.update(create_food(food_per_turn))
        offspring = []
        survivors = []

        for c in chij:
            c.move()
            c.age += 1
            c.eat(food)

            if c.is_alive():
                survivors.append(c)

                if c.energy >= reproduction_energy:
                    child = reproduce(c)
                    offspring.append(child)

        chij = survivors + offspring
        turns_completed = turn

        if chij:
            highest_generation = max(
                highest_generation,
                max(c.generation for c in chij)
            )

    return {
        "turns": turns_completed,
        "final_population": len(chij),
        "extinct": len(chij) == 0,
        "highest_generation": highest_generation,
        "average_energy": (
            statistics.mean(c.energy for c in chij)
            if chij else 0
        ),
        "average_speed": (
            statistics.mean(c.speed for c in chij)
            if chij else 0
        ),
        "average_efficiency": (
            statistics.mean(c.efficiency for c in chij)
            if chij else 0
        ),
        "food_remaining": len(food)
    }


def run_experiment(number_of_runs=100000):
    results = []

    print(f"Running {number_of_runs:,} simulations...")

    for i in range(number_of_runs):
        result = main()
        results.append(result)

        if (i + 1) % 2000 == 0:
            print(f"Completed: {i + 1:,}/{number_of_runs:,}")

    populations = [r["final_population"] for r in results]
    generations = [r["highest_generation"] for r in results]
    turns = [r["turns"] for r in results]

    extinct_count = sum(r["extinct"] for r in results)
    survived_count = number_of_runs - extinct_count

    print("\n" + "=" * 50)
    print("WORLD SIMULATION: FINAL REPORT")
    print("=" * 50)

    print(f"Total simulations: {number_of_runs:,}")
    print(f"Extinctions: {extinct_count:,} "
          f"({extinct_count / number_of_runs * 100:.2f}%)")
    print(f"Survived to the end: {survived_count:,} "
          f"({survived_count / number_of_runs * 100:.2f}%)")

    print("\nPOPULATION")
    print(f"Average final population: {statistics.mean(populations):.2f}")
    print(f"Minimum final population: {min(populations)}")
    print(f"Maximum final population: {max(populations)}")

    print("\nEVOLUTION")
    print(f"Average highest generation: {statistics.mean(generations):.2f}")
    print(f"Highest generation observed: {max(generations)}")

    print("\nSURVIVAL")
    print(f"Average turns completed: {statistics.mean(turns):.2f}")
    print(f"Runs reaching turn {max_turns}: "
          f"{sum(t == max_turns for t in turns):,}")

    print("\nOTHER AVERAGES")
    print(f"Average final food: "
          f"{statistics.mean(r['food_remaining'] for r in results):.2f}")
    print(f"Average energy of surviving organisms: "
          f"{statistics.mean([r['average_energy'] for r in results if r['final_population'] > 0]):.2f}"
          if survived_count else "Average energy: no survivors")
    print(f"Average speed of surviving organisms: "
          f"{statistics.mean([r['average_speed'] for r in results if r['final_population'] > 0]):.2f}"
          if survived_count else "Average speed: no survivors")
    print(f"Average efficiency of surviving organisms: "
          f"{statistics.mean([r['average_efficiency'] for r in results if r['final_population'] > 0]):.2f}"
          if survived_count else "Average efficiency: no survivors")

    with open("simulation_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\nDetailed results saved to simulation_results.csv")


if __name__ == "__main__":
    run_experiment(100000)
        