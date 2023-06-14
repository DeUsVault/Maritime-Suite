#include "GeneticAlgorithm.h"
#include <iomanip>

GeneticAlgorithm::GeneticAlgorithm(TArray<TArray<float>> heightmap_file, TArray<TArray<float>> initial_grid, string radars_file, int _maxGenerations, int _populationSize, int _mutationRate,
	double _fitness_target, double _coverage_weight, double _cost_weight, int _max_radars_to_use, int _min_radars_to_use)
{
	mutationRate = _mutationRate;
	maxGenerations = _maxGenerations;
	grid = Grid(heightmap_file, initial_grid, radars_file);
	totalRadars = grid.radii.size();
	areaSize = grid.heightmap.size();
	fitness_target = _fitness_target;
	population = Population(_populationSize, totalRadars, areaSize, &grid, _coverage_weight, _cost_weight, _max_radars_to_use, _min_radars_to_use);
}

void GeneticAlgorithm::Fit()
{
	population.CalculateFitness();
	
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> distr(0, 100);

	//cout << "Fitness tolerance: " << fitness_target << endl;
	//cout << "Max Generations: " << maxGenerations << endl;
	//cout << "Population size: " << population.populationSize << endl;
	//cout << "Mutation Rate: " << mutationRate << endl;

	while (population.fitness < fitness_target && generation < maxGenerations)
	{
		Selection();
		CrossOver();
		Mutation();
		AddFittestOffspring();
		population.CalculateFitness();
		generation++;
		//cout << "Generation: " << generation << " Fitness: " << std::fixed << std::setprecision(2) << population.fitness << endl;
	}
}

vector<Point> GeneticAlgorithm::GetSolutionRadarPositions()
{
	return population.GetFittest().GetRadarPositions();
}

vector<bool> GeneticAlgorithm::GetSolutionUseRadars()
{
	return population.GetFittest().GetUseRadars();
}

void GeneticAlgorithm::DisplayCoverageMap()
{
	grid.PrintCoverageMap();
}

float GeneticAlgorithm::Coverage()
{
	return grid.ComputeCoveragePercentage(population.GetFittest().GetRadarPositions(), population.GetFittest().GetUseRadars());
}

float GeneticAlgorithm::Cost()
{
	return grid.ComputeTotalCost(population.GetFittest().GetUseRadars());
}

void GeneticAlgorithm::Selection()
{
	fittest = population.GetFittest();
	secondFittest = population.GetSecondFittest();
}

 void GeneticAlgorithm::CrossOver()
{
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> distr(1, totalRadars-1);
	// Number of radars to split the chromosome
	int crossOverPoint = distr(gen) * 65;

	// 65 bits to describe each radar, 
	// We split the fittest chromosome in a way that all the bits for a radar is exchanged with the second fittest chromosome

	//Swap values among parents
	for (int i = 0; i < crossOverPoint; i++)
	{
		int temp = fittest.genes[i];
		fittest.genes[i] = secondFittest.genes[i];
		secondFittest.genes[i] = temp;
	}
}


void GeneticAlgorithm::Mutation()
{
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> mutation_distr(0, 100);

	// Flip bits for all radars in the chromosome with a given mutation rate
	for (int radar = 0; radar < fittest.totalRadars; radar++) {
		
		if (mutation_distr(gen) < mutationRate) {
			// Flip one bit in the first 32 bits (representing x position)
			std::uniform_int_distribution<> x_distr( (65*radar), 32 + (65*radar) );
			int x_index = x_distr(gen);
			// Flip the selected bit
			fittest.genes[x_index] = fittest.genes[x_index] == 0 ? 1 : 0;
		}
		if (mutation_distr(gen) < mutationRate) {
			// Flip one bit in the second 32 bits (representing y position)
			std::uniform_int_distribution<> y_distr((65 * radar) + 32, 32 + (65 * radar) + 32);
			int y_index = y_distr(gen);
			fittest.genes[y_index] = fittest.genes[y_index] == 0 ? 1 : 0;
		}
		if (mutation_distr(gen) < mutationRate) {
			// Flip is used bit of the radar
			//fittest.genes[radar*64] = fittest.genes[radar * 64] == 0 ? 1 : 0;
			fittest.genes[radar * 65] = fittest.genes[radar * 65] == 0 ? 1 : 0;
		}
	}

	// Do the same for the second fittest chromosome

	for (int radar = 0; radar < secondFittest.totalRadars; radar++) {
		if (mutation_distr(gen) < mutationRate) {
			// Select a random index in the first 32 bits
			std::uniform_int_distribution<> x_distr((65 * radar), 32 + (65 * radar));
			int x_index = x_distr(gen);
			// Flip the selected bit
			secondFittest.genes[x_index] = secondFittest.genes[x_index] == 0 ? 1 : 0;
		}
		if (mutation_distr(gen) < mutationRate) {
			std::uniform_int_distribution<> y_distr((65 * radar) + 32, 32 + (65 * radar) + 32);
			int y_index = y_distr(gen);
			secondFittest.genes[y_index] = secondFittest.genes[y_index] == 0 ? 1 : 0;
		}
		if (mutation_distr(gen) < mutationRate) {
			// Flip is used bit of the radar
			secondFittest.genes[radar * 65] = secondFittest.genes[radar * 65] == 0 ? 1 : 0;
		}
	}
}


//void GeneticAlgorithm::AddFittestOffspring()
//{	
//	/* This function decides which is the fittest between the two offspring and 
//	replace the least fittest chromosome in the population with the fittest offspring*/
//
//	fittest.CalculateFitness();
//	secondFittest.CalculateFitness();
//
//	fittest = fittest.fitness > secondFittest.fitness ? fittest : secondFittest;
//
//
//	int leastFittestIndex = population.GetLeastFittestIndex();
//
//	population.individuals[leastFittestIndex] = fittest;
//}
 

void GeneticAlgorithm::AddFittestOffspring()
{	
	/* This function replaces the two least fittest chromosomes in the population with the two offspring. */

	fittest = fittest.fitness > secondFittest.fitness ? fittest : secondFittest;

	int leastFittestIndex = population.GetLeastFittestIndex();

	population.individuals[leastFittestIndex] = fittest;

	int penultimateFittestIndex = population.GetLeastFittestIndex();
	population.individuals[penultimateFittestIndex] = secondFittest;

}