package dev.ibukun.risk;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.List;

public record RiskRequest(@NotNull @Size(min = 30, max = 30) List<Double> features) {}
