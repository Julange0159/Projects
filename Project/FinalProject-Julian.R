set.seed(1818)
library('rsample')
library('ggplot2')
library('dplyr')
library('ISLR')
library('tidyverse')

#--------------------------------------------------------
# Classification
#--------------------------------------------------------
spotify_df <- 
  read.csv(here::here("datasets",
                      "tracks_hit.csv"))

spotify_df <- spotify_df %>% as_tibble() %>% mutate(hit = as.factor(hit))

spotify_split <- initial_split(spotify_df, prop = 0.75)
spotify_train <- training(spotify_split)
spotify_test <- testing(spotify_split)

logit_fit1 <- glm(hit ~ acousticness + danceability + energy + liveness + loudness
                  + instrumentalness + speechiness + tempo + valence,
                  family = binomial,
                  data = spotify_train)

summary(logit_fit1)
(exp(logit_fit1$coefficients[-1])-1)*100


#--------------------------------------------------------
# ROC Curve
#--------------------------------------------------------
library('plotROC')
preds_train <- predict(logit_fit1, newdata = spotify_train, type = "response")
preds_test <- predict(logit_fit1, newdata = spotify_test, type = "response")

head(preds_train)
head(preds_test)

results_train <- data.frame(
  `truth` = spotify_train   %>% select(hit) %>% 
    mutate(hit = as.numeric(hit)),
  `Class1` =  preds_train,
  `type` = rep("train",length(preds_train))
)

results_test <- data.frame(
  `truth` = spotify_test   %>% select(hit) %>% 
    mutate(hit = as.numeric(hit)),
  `Class1` =  preds_test,
  `type` = rep("test",length(preds_test))
)

results <- bind_rows(results_train,results_test)

results_train %>% slice(1:10)
results_test %>% slice(1:10)

p <- ggplot(results, 
            aes(m = Class1, d = as.numeric(hit), color = type)) + 
  geom_roc(labelsize = 3.5, 
           cutoffs.at = 
             c(0.99,0.9,0.7,0.5,0.3,0.1,0)) +
  theme_minimal(base_size = 16)
print(p)
calc_auc(p)
#--------------------------------------------------------
# Random Forest
#--------------------------------------------------------
library('randomForest')
library('randomForestExplainer')
rf_mods <- list()
oob_err <- NULL
test_err <- NULL
for(mtry in 1:9){
  rf_fit <- randomForest(hit ~ acousticness + danceability + energy + liveness + loudness
                         + instrumentalness + speechiness + tempo + valence,
                         data = spotify_train,
                         mtry = mtry,
                         na.action = na.roughfix,
                         ntree = 600)
  oob_err[mtry] <- rf_fit$err.rate[600]
  
  cat(mtry," ")
}

results_DF <- data.frame(mtry = 1:9, oob_err)
ggplot(results_DF, aes(x = mtry, y = oob_err)) + geom_point() + theme_minimal()



rf_fit <- randomForest(hit ~ acousticness + danceability + energy + liveness + loudness
                       + instrumentalness + speechiness + tempo + valence, 
                       data = spotify_df,
                       type = classification,
                       mtry = 3,
                       na.action = na.roughfix,
                       ntree = 300, 
                       importance = TRUE)

rf_fit

par(mar=c(2,2,2,2))

plot(rf_fit)

feat_imp_df <- importance(rf_fit) %>% 
  data.frame() %>% 
  mutate(feature = row.names(.)) 

# plot dataframe
ggplot(feat_imp_df, aes(x = reorder(feature, MeanDecreaseGini), 
                        y = MeanDecreaseGini) ) +
  geom_bar(stat='identity', fill = '#1DB954FF') +
  coord_flip() +
  theme_classic() +
  labs(
    x     = "Features",
    y     = "Importance",
    title = "Feature Importance: <Random Forest>"
  )

plot_min_depth_distribution(rf_fit)
