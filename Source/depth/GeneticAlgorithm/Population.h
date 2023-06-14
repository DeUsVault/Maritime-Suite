#pragma once
#include <vector>
#include <random>
#include "Individual.h"
#include "Grid.h"

using namespace std;

class Population
{
public:
	vector<Individual> individuals;
	int populationSize;
	int totalRadars;
	int areaSize;
	int geneSize;
	double fitness;
	Grid* grid;

	Population();

	Population(int size, int totalRadars, int areaSize, Grid* _grid, double _coverage_weight, double _cost_weight);

	void InitializeRandomPopulation(double _coverage_weight, double _cost_weight);

	int GetFittestIndex();
	Individual GetFittest();

	int GetSecondFittestIndex();
	Individual GetSecondFittest();

	int GetLeastFittestIndex();
	Individual GetLeastFittest();

	void CalculateFitness();
};
