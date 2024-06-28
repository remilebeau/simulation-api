import numpy as np

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# configure CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @desc returns 1000 random values from a triangular distribution
# @route GET /api/distributions/triangular
# @access public
@app.get("/api/distributions/triangular")
def distribution_triangular(distMin: int, distMode: int, distMax: int):
    # set seed
    rng = np.random.default_rng(seed=42)
    # check min <= mode and mode <= max and min < max
    if not (distMin <= distMode and distMode <= distMax and distMin < distMax):
        raise HTTPException(
            status_code=400,
            detail="Please ensure the following: distMin <= distMode <= distMax; and distMin < distMax",
        )
    # generate distribution
    distValues = rng.triangular(distMin, distMode, distMax, 1000).tolist()
    return {"distValues": distValues}


# @desc returns the sum of simPeriodsPerYear samples from a triangular distribution
# @route GET /api/simulations/
# @access public
@app.get("/api/simulations/triangular")
def simulation_triangular(
    distMin: int, distMode: int, distMax: int, simPeriodsPerYear: int
):
    # set seed
    rng = np.random.default_rng(seed=42)
    # check min <= mode and mode <= max and min < max
    if not (distMin <= distMode and distMode <= distMax and distMin < distMax):
        raise HTTPException(
            status_code=400,
            detail="Please ensure the following: distMin <= distMode <= distMax; and distMin < distMax",
        )

    # generate distribution
    dist = rng.triangular(distMin, distMode, distMax, 1000)

    #   take simPeriodsPerYear samples from the distribution and return their sum. 1000 simValues in total
    simValues = []
    for i in range(0, 1000):
        simValues.append(float(rng.choice(dist, simPeriodsPerYear).sum()))

    # generate stats
    simMin = round(np.min(simValues))
    simMax = round(np.max(simValues))
    simMean = round(np.mean(simValues))
    simQ1 = round(np.percentile(simValues, 25).round(0))
    simQ2 = round(np.percentile(simValues, 50).round(0))
    simQ3 = round(np.percentile(simValues, 75).round(0))
    lowerCI = round(
        np.mean(simValues) - 1.96 * np.std(simValues) / np.sqrt(len(simValues))
    )
    upperCI = round(
        np.mean(simValues) + 1.96 * np.std(simValues) / np.sqrt(len(simValues))
    )

    return {
        "simValues": simValues,
        "simMin": simMin,
        "simMax": simMax,
        "simMean": simMean,
        "simQ1": simQ1,
        "simQ2": simQ2,
        "simQ3": simQ3,
        "lowerCI": lowerCI,
        "upperCI": upperCI,
    }


# @desc returns 1000 random values from a uniform distribution
# @route GET /api/distributions/uniform
# @access public
@app.get("/api/distributions/uniform")
def distribution_uniform(distMin: int, distMax: int):
    # set seed
    rng = np.random.default_rng(seed=42)
    # check min < max
    if not (distMin < distMax):
        raise HTTPException(
            status_code=400,
            detail="Please ensure the following: distMin < distMax",
        )
    # generate distribution
    distValues = rng.uniform(distMin, distMax, 1000).tolist()
    return {"distValues": distValues}


# @desc returns the sum of simPeriodsPerYear samples from a uniform distribution
# @route GET /api/simulations/
# @access public
@app.get("/api/simulations/uniform")
def simulation_uniform(distMin: int, distMax: int, simPeriodsPerYear: int):
    # set seed
    rng = np.random.default_rng(seed=42)
    # check min < max
    if not (distMin < distMax):
        raise HTTPException(
            status_code=400,
            detail="Please ensure the following: distMin < distMax",
        )

    # generate distribution
    dist = rng.uniform(distMin, distMax, 1000)

    #   take simPeriodsPerYear samples from the distribution and return their sum. 1000 simValues in total
    simValues = []
    for i in range(0, 1000):
        simValues.append(float(rng.choice(dist, simPeriodsPerYear).sum()))

    # generate stats
    simMin = round(np.min(simValues))
    simMax = round(np.max(simValues))
    simMean = round(np.mean(simValues))
    simQ1 = round(np.percentile(simValues, 25).round(0))
    simQ2 = round(np.percentile(simValues, 50).round(0))
    simQ3 = round(np.percentile(simValues, 75).round(0))
    lowerCI = round(
        np.mean(simValues) - 1.96 * np.std(simValues) / np.sqrt(len(simValues))
    )
    upperCI = round(
        np.mean(simValues) + 1.96 * np.std(simValues) / np.sqrt(len(simValues))
    )

    return {
        "simValues": simValues,
        "simMin": simMin,
        "simMax": simMax,
        "simMean": simMean,
        "simQ1": simQ1,
        "simQ2": simQ2,
        "simQ3": simQ3,
        "lowerCI": lowerCI,
        "upperCI": upperCI,
    }


# @desc returns 1000 random values from a truncated normal distribution
# @route GET /api/distributions/truncated_normal
# @access public
@app.get("/api/distributions/truncated_normal")
def distribution_truncated_normal(
    distMin: int, distMean: int, distMax: int, distSD: float
):
    # check distSD >= 0
    if not (distSD >= 0):
        raise HTTPException(
            status_code=400,
            detail="Standard deviation must be non-negative",
        )

    # set seed
    rng = np.random.default_rng(seed=42)

    # generate normal distribution to truncate
    norm_vals = rng.normal(distMean, distSD, 1000).tolist()

    # truncate with custom function
    def truncated_normal(norm_vals):
        value = rng.choice(norm_vals)
        if not (distMin <= value and value <= distMax):
            value = truncated_normal(norm_vals)
        return value

    # generate distribution
    distValues = []
    for i in range(0, 1000):
        distValues.append(truncated_normal(norm_vals))

    print(distValues)
    return {"distValues": distValues}


# @desc returns the sum of simPeriodsPerYear samples from a truncated normal distribution
# @route GET /api/simulations/
# @access public
@app.get("/api/simulations/truncated_normal")
def simulation_truncated_normal(
    distMin: int, distMean: int, distMax: int, distSD: float, simPeriodsPerYear: int
):
    # check distSD >= 0
    if not (distSD >= 0):
        raise HTTPException(
            status_code=400,
            detail="Standard deviation must be non-negative",
        )

    # set seed
    rng = np.random.default_rng(seed=42)

    # generate normal distribution to truncate
    norm_vals = rng.normal(distMean, distSD, 1000)

    # truncate with custom function
    def truncated_normal(dist):
        value = rng.choice(dist, 1)
        if not (distMin <= value and value <= distMax):
            value = truncated_normal(dist)
        return value

    # generate distribution
    dist = []
    for i in range(0, 1000):
        dist.append(truncated_normal(norm_vals))

    #   take simPeriodsPerYear samples from the distribution and return their sum. 1000 simValues in total
    simValues = []
    for i in range(0, 1000):
        simValues.append(float(rng.choice(dist, simPeriodsPerYear).sum()))

    # generate stats
    simMin = round(np.min(simValues))
    simMax = round(np.max(simValues))
    simMean = round(np.mean(simValues))
    simQ1 = round(np.percentile(simValues, 25).round(0))
    simQ2 = round(np.percentile(simValues, 50).round(0))
    simQ3 = round(np.percentile(simValues, 75).round(0))
    lowerCI = round(
        np.mean(simValues) - 1.96 * np.std(simValues) / np.sqrt(len(simValues))
    )
    upperCI = round(
        np.mean(simValues) + 1.96 * np.std(simValues) / np.sqrt(len(simValues))
    )

    return {
        "simValues": simValues,
        "simMin": simMin,
        "simMax": simMax,
        "simMean": simMean,
        "simQ1": simQ1,
        "simQ2": simQ2,
        "simQ3": simQ3,
        "lowerCI": lowerCI,
        "upperCI": upperCI,
    }
