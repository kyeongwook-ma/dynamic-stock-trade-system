import math

# update weight vector & return it
def exp_gradient(weight, opening, closing, rate, N):
	
	def get_weight_vector(weight):
		# weight is the vector of weights at time t
		# x is the vector of relative performance of all the stocks over the course of day t
		self.x = closing / opening

		for i in range(0,N) :
			num = weight[i] * math.exp( rate * x[i] / weight * x) 
			denum = 0

			for j in N:
				denom += weight[j] * math.exp(rate * x[j] / weight * x)

		return num / denum

	# update in exponatiated gradient manner
	weight[t+1] = get_weight_vector(weight[t])

	return weight