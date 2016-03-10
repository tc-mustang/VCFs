PL = function(x, error){ #, where x is a character vector of length one: "REFcount, ALTcount"
  REFcount <- as.numeric(unlist(strsplit(x,","))[1])
  ALTcount <- as.numeric(unlist(strsplit(x,","))[2])
  n = REFcount + ALTcount
  if(n == 0) return(setNames(rep(".", 3), c("0/0","0/1","1/1"))) else
    k <- ALTcount 
  e <- error 
  L <- c("L_AA"=choose(n, k) * e^k * (1-e)^(n-k), 
         "L_AB"=choose(n, k) * (0.50)^k * (0.50)^(n-k),
         "L_BB"=choose(n, n-k) * (1-e)^k * e^(n-k)) 
  normL <- setNames(L/max(L), c("0/0","0/1","1/1"))
  return(round(-10*log10(normL)))
}

