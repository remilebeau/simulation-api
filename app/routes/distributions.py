from fastapi import APIRouter, HTTPException
import numpy as np
from ..utils.utils import is_triangular, determine_distribution

router = APIRouter(
    prefix="/api/distributions",
    tags=["distributions"],
    responses={404: {"description": "Not found"}},
)


# @desc returns 1000 random values
# @route GET /api/distributions/random
# @access public
@router.get("/random")
def distribution_random(min: float = 0, mean: float = 0, max: float = 0, sd: float = 0):
    """
    Returns 1000 pseudorandom values based on the given parameters.
    The parameters must fit a triangular, normal, uniform, or truncated normal distribution.\n

    Args:\n
        min (float): The minimum value of the distribution.\n
        mean (float): The mean of the distribution.\n
        max (float): The maximum value of the distribution.\n
        sd (float): The standard deviation of the distribution.\n

    Returns:\n
        distValues (list): A list of 1000 pseudorandom values based on the given parameters.\n
        distribution (str): The distribution used to generate the values.\n

    Raises:\n
        HTTPException: If the inputs do not satisfy one of the following sets of conditions:

        triangular:
            min <= mean <= max
            min < max
            sd = 0

        normal:
            sd > 0
            min = 0
            max = 0

        truncated normal:
            min <= mean <= max
            min < max
            sd > 0

        uniform:
            min < max
            mean = 0
            sd = 0
    """
    rng = np.random.default_rng(seed=42)

    # custom function for truncated normal
    def truncated_normal(min, mean, max, sd):
        value = rng.normal(mean, sd)
        if value < min or value > max:
            value = truncated_normal(min, max, mean, sd)
        return value

    distribution = determine_distribution(min, mean, max, sd)
    if distribution == "normal":
        values = rng.normal(mean, sd, 1000).tolist()
        return {"distribution": distribution, "distValues": values}
    elif distribution == "uniform":
        values = rng.uniform(min, max, 1000).tolist()
        return {"distribution": distribution, "distValues": values}
    elif distribution == "triangular":
        values = rng.triangular(min, mean, max, 1000).tolist()
        return {"distribution": distribution, "distValues": values}
    elif distribution == "truncated normal":
        values = [truncated_normal(min, mean, max, sd) for _ in range(1000)]
        return {"distribution": distribution, "distValues": values}
    else:
        raise HTTPException(status_code=400, detail="unknown distribution")


# @desc returns 1000 random values from a triangular distribution
# @route GET /api/distributions/triangular
# @access public
@router.get("/triangular")
def distribution_triangular(distMin: float, distMode: float, distMax: float):
    """
    Returns 1000 pseudorandom values from a triangular distribution.

    Args:\n
        distMin (float): The minimum value of the distribution.\n
        distMode (float): The mode value of the distribution.\n
        distMax (float): The maximum value of the distribution.\n

    Returns:\n
        distValues (list): A list of 1000 pseudorandom values from a triangular distribution.

    Raises:\n
        HTTPException: If the input values do not satisfy the following conditions:
            distMin <= distMode <= distMax
            distMin < distMax
            A 400 status code and an error message are returned in this case.
    """
    # set seed
    rng = np.random.default_rng(seed=42)
    # validate data
    if not is_triangular(distMin, distMode, distMax):
        raise HTTPException(
            status_code=400,
            detail="Please ensure the following: 1) distMin <= distMode <= distMax 2) distMin < distMax",
        )
    # generate distribution
    distValues = rng.triangular(distMin, distMode, distMax, 1000).tolist()
    return {"distValues": distValues}


# @desc returns 1000 random values from a uniform distribution
# @route GET /api/distributions/uniform
# @access public
@router.get("/uniform")
def distribution_uniform(distMin: int, distMax: int):
    """
    Returns 1000 pseudorandom values from a uniform distribution.

    Args:\n
        distMin (int): The minimum value of the distribution.\n
        distMax (int): The maximum value of the distribution.\n

    Returns:\n
        distValues (list): A list of 1000 pseudorandom values from a uniform distribution.

    Raises:\n
        HTTPException: If the input values do not satisfy the following condition:
            distMin < distMax
            A 400 status code and an error message are returned in this case.
    """
    # set seed
    rng = np.random.default_rng(seed=42)
    # validate data
    if distMin >= distMax:
        raise HTTPException(
            status_code=400,
            detail="Please ensure the following: distMin < distMax",
        )
    # generate distribution
    distValues = rng.uniform(distMin, distMax, 1000).tolist()
    return {"distValues": distValues}


# @desc returns 1000 random values from a normal distribution
# @route GET /api/distributions/normal
# @access public
@router.get("/normal")
def distribution_normal(distMean: float, distSD: float):
    """
    Returns 1000 pseudorandom values from a normal distribution.

    Args:\n
        distMean (float): The mean value of the distribution.\n
        distSD (float): The standard deviation of the distribution.\n

    Returns:\n
        distValues (list): A list of 1000 pseudorandom values from a normal distribution.

    Raises:\n
        HTTPException: If the input values do not satisfy the following conditions:
            distSD > 0
            A 400 status code and an error message are returned in this case.
    """
    # validate data
    if distSD <= 0:
        raise HTTPException(
            status_code=400,
            detail="Please ensure the following: distSD > 0",
        )

    # set seed
    rng = np.random.default_rng(seed=42)

    # generate distribution
    distValues = rng.normal(distMean, distSD, 1000).tolist()

    return {"distValues": distValues}


# @desc returns 1000 random values from a truncated normal distribution
# @route GET /api/distributions/truncated_normal
# @access public
@router.get("/truncated_normal")
def distribution_truncated_normal(
    distMin: float, distMean: float, distMax: float, distSD: float
):
    """
    Returns 1000 pseudorandom values from a truncated normal distribution.

    Args:\n
        distMin (float): The minimum value of the distribution.\n
        distMean (float): The mean value of the distribution.\n
        distMax (float): The maximum value of the distribution.\n
        distSD (float): The standard deviation of the distribution.\n

    Returns:\n
        distValues (list): A list of 1000 pseudorandom values from a truncated normal distribution.

    Raises:\n
        HTTPException: If the input values do not satisfy the following conditions:
            distMin <= distMean
            distMean <= distMax
            distMin < distMax
            distSD > 0
            A 400 status code and an error message are returned in this case.
    """
    # validate data
    if not is_triangular(distMin, distMean, distMax) or distSD <= 0:
        raise HTTPException(
            status_code=400,
            detail="Please ensure the following: 1) distMin <= distMean <= distMax 2) distMin < distMax 3) distSD > 0",
        )

    # set seed
    rng = np.random.default_rng(seed=42)

    # truncate with custom function
    def truncated_normal(min, mean, max, sd):
        value = rng.normal(mean, sd)
        if value < min or value > max:
            value = truncated_normal(min, max, mean, sd)
        return value

    # generate distribution
    distValues = [
        truncated_normal(distMin, distMax, distMean, distSD) for _ in range(0, 1000)
    ]

    return {"distValues": distValues}
