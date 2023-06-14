// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "GeneticAlgorithm/GeneticAlgorithm.h"
#include <array>
#include "CSV_Exporter.generated.h"

/**
 * 
 */
UCLASS()
class MARITIMESIMULATION_API UCSV_Exporter : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
		UFUNCTION(BlueprintCallable, Category = "save")
		static bool FileSaveString(FString SaveTextB, FString FileNameB);

	UFUNCTION(BlueprintPure, Category = "save")
		static bool FileLoadString(FString FileNameA, FString& SaveTextA);

	UFUNCTION(BlueprintCallable, Category = "save")
		static TArray<FVector> Genetic(TArray<float> Grid, TArray<int> InitialGrid, int32 Width, int32 Height, FString Radar_list, int _maxGenerations, int _populationSize, int _mutationRate, double _fitness_target, double area_coverage_weight, double cost_weight, int _max_radars_to_use, int _min_radars_to_use, FVector2D& score);
};
