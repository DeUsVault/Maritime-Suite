// Fill out your copyright notice in the Description page of Project Settings.


#include "CSV_Exporter.h"
#include <depth/GeneticAlgorithm/GeneticAlgorithm.h>
bool UCSV_Exporter::FileSaveString(FString SaveTextB, FString FileNameB)
{
	return FFileHelper::SaveStringToFile(SaveTextB, *(FPaths::ProjectDir() + "/Source/depth/GeneticAlgorithm/" + FileNameB));
}

bool UCSV_Exporter::FileLoadString(FString FileNameA, FString& SaveTextA)
{
	return FFileHelper::LoadFileToString(SaveTextA, *(FPaths::ProjectDir() + "/Coverage/" + FileNameA));
}

TArray<TArray<float>> ConvertTo2DArray(const TArray<float>& InputArray, int32 Width, int32 Height)
{
	TArray<TArray<float>> OutputArray;

	int32 Index = 0;
	int32 Row, Column;
	for (Row = 0; Row < Height; ++Row)
	{
		TArray<float> RowArray;
		for (Column = 0; Column < Width; ++Column)
		{
			RowArray.Add(InputArray[Index]);
			++Index;
		}
		OutputArray.Add(RowArray);
	}

	return OutputArray;
}

TArray<TArray<int>> ConvertTo2DArray(const TArray<int>& InputArray, int32 Width, int32 Height)
{
	TArray<TArray<int>> OutputArray;

	int32 Index = 0;
	int32 Row, Column;
	for (Row = 0; Row < Height; ++Row)
	{
		TArray<int> RowArray;
		for (Column = 0; Column < Width; ++Column)
		{
			RowArray.Add(InputArray[Index]);
			++Index;
		}
		OutputArray.Add(RowArray);
	}

	return OutputArray;
}

TArray<FVector> UCSV_Exporter::Genetic(TArray<float> Grid, TArray<int> InitialGrid, int32 width, int32 height, FString Radar_list, int _maxGenerations, int _populationSize, int _mutationRate, double _fitness_target, double _area_coverage_weight, double _cost_weight, int _max_radars_to_use, int _min_radars_to_use, FVector2D& score)
{
	//string Grid_formatted = string(TCHAR_TO_UTF8(*Grid));
	string Radar_formatted = string(TCHAR_TO_UTF8(*Radar_list));
	TArray<TArray<float>> grid = ConvertTo2DArray(Grid, width, height);
	TArray<TArray<int>> initial_grid = ConvertTo2DArray(InitialGrid, width, height);
	GeneticAlgorithm GA(grid, initial_grid, Radar_formatted, _maxGenerations, _populationSize, _mutationRate, _fitness_target, _area_coverage_weight, _cost_weight, _max_radars_to_use, _min_radars_to_use);
	GA.Fit();
	UPROPERTY() 
	TArray<FVector> temp;
	std::vector<Point> _Positions = GA.GetSolutionRadarPositions();
	std::vector<bool> _active_radars = GA.GetSolutionUseRadars();
	for (uint j = 0; j < _Positions.size(); j++) {
		FVector Point_(_Positions[j].x, _Positions[j].y, _active_radars[j]);
		temp.Add(Point_);
	}
	double coverage = GA.Coverage();
	score.X= GA.Coverage();
	score.Y = GA.Cost();
	UE_LOG(LogTemp, Warning, TEXT("Coverage : %.2f"), coverage);

	return temp;
}


