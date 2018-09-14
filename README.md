This both calculates the likelihood of "busting" when using the Martingale strategy, given n bets, as well as simulates the process as a cross reference.

The calculation is done within the class martingale. This class calculates the number of consecutive losses before your balance is gone. The result should be an accurate figure of the likelihood of x consecutive losses, however there are other ways to lose using the martingale strategy than x consecutive losses, which is not account for by this formula. For example if 5 consecutive losses leaves you with a lower remaining bank than your next stake, you can still continue however the next run of consecutive losses need may be less than the initial result. 

The game class is the monte carlo simulation done. This works by doubling the stake everytime a loss is seen and reverting to the starting after a win. The final result returns the percentage of times you returned a lower balance that your starting stake, when you lost everything and when you lost some but not all of your bank.

The game simulation should return a higher figure both because of the reasons details above in the second paragraph and becasue the last run of games can eat into your abnk without busting you. 

As an example if you start with a bank of 300 using a stake of 1, you should go "bust" after 8 consecutive loses. The likelihood is 17% of getting 8 consecutive losses. Running the simulation we get the following results; 20.3% that my final balance will be less, 17% of losing the entire balance, 3.3% of a final balance being lowere than starting but not 0.
