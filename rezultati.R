library(ggplot2)
library(dplyr)

podaci <- read.csv("rezultati_prosiriti.csv")

minio_podaci <- podaci %>% 
  filter(Sistem == "MinIO", Iteracija > 1)

model_lm <- lm(Vreme_s ~ Velicina_MB + Broj_fajlova, data = minio_podaci)

cat("\n=== SUMMARY MODELA ===\n")
print(summary(model_lm))

minio_podaci$Predvidjeno <- predict(model_lm)
greske <- minio_podaci$Vreme_s - minio_podaci$Predvidjeno

rmse_val <- sqrt(mean(greske^2))
mae_val <- mean(abs(greske))

cat("\nMETRIKE GREŠKE MODELA\n")
cat(sprintf("RMSE (Root Mean Square Error): %.4f s\n", rmse_val))
cat(sprintf("MAE  (Mean Absolute Error):     %.4f s\n", mae_val))

ggplot(minio_podaci, aes(x = Vreme_s, y = Predvidjeno, color = Scenario)) +
  geom_point(size = 2.5, alpha = 0.7) +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "red") +
  theme_minimal() +
  labs(
    title = "Nova evaluacija regresije sa proširenim datasetom",
    subtitle = sprintf("RMSE: %.4f s | MAE: %.4f s", rmse_val, mae_val),
    x = "Stvarno vreme (s)",
    y = "Predviđeno vreme modela (s)"
  )
proseci <- podaci %>%
  filter(Iteracija > 1) %>%
  group_by(Scenario, Sistem, Velicina_MB) %>%
  summarise(prosek_vreme = mean(Vreme_s), .groups = 'drop')

ggplot(proseci, aes(x = reorder(Scenario, Velicina_MB), y = prosek_vreme, fill = Sistem)) +
  geom_bar(stat = "identity", position = "dodge", width = 0.7) +
  geom_text(aes(label = sprintf("%.2fs", prosek_vreme)), 
            position = position_dodge(width = 0.7), 
            vjust = -0.5, size = 3) +
  theme_minimal() +
  labs(
    title = "Poređenje prosečnog vremena izvršavanja: Lokalno vs MinIO",
    subtitle = "Obuhvaćeni svi scenariji",
    x = "Scenario (test)",
    y = "Prosečno vreme (s)",
    fill = "Sistem"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))