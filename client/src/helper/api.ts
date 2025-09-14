import axios from "axios";

export const loginUser = async (email: string, password: string) => {
  try {
    const response = await axios.post(
      "/auth/login",
      { email, password },
      { withCredentials: true }
    );
    if (response.status !== 200) {
      console.log("Something went wrong while logging in.");
    }
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const regiterUser = async (
  username: string,
  email: string,
  password: string
) => {
  try {
    const response = await axios.post(
      "/auth/register",
      {
        username,
        email,
        password,
      },
      { withCredentials: true }
    );
    if (response.status !== 200) {
      console.log("Something went wrong while siging in.");
    }
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getUserProfile = async () => {
  try {
    const response = await axios.post("/auth/verify");
    if (response.status !== 200) {
      console.log("Something went wrong while getting user profile.");
    }
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const logoutUser = async () => {
  try {
    const response = await axios.post("/auth/logout");
    if (response.status !== 200) {
      console.log("Something went wrong while logging out.");
    }
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const addToFavorites = async (
  name: string,
  description: string,
  recipe: string[],
  image: string | null
) => {
  try {
    const response = await axios.post("/favorite/add", {
      name,
      description,
      recipe,
      image,
    });
    if (response.status !== 200) {
      console.log("Something went wrong while adding to favorites.");
    }
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const removeFromFavorites = async (favoriteId: number) => {
  try {
    const response = await axios.post("favorite/remove", { id: favoriteId });
    if (response.status !== 200) {
      console.log("Something went wrong while removing from favorites.");
    }
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getFavoritesOfUser = async () => {
  try {
    const response = await axios.get("favorite/get-all");
    if (response.status !== 200) {
      console.log("Something went wrong while getting favorites.");
    }
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getSuggetions = async (item: string[], info: string) => {
  try {
    const reponse = await axios.post("/suggest/ingredients", {
      item,
      info,
    });
    if (reponse.status !== 200) {
      console.log(
        "Something went wrong while getting suggetions by ingredients."
      );
    }
    return reponse;
  } catch (error) {
    console.log(error);
  }
};

export const getSuggetionsByName = async (text: string) => {
  try {
    const reponse = await axios.post("/suggest/prompt", { text });
    if (reponse.status !== 200) {
      console.log(
        "Something went wrong while getting suggetions ny dish name."
      );
    }
    return reponse;
  } catch (error) {
    console.log(error);
  }
};

export const fullRecipe = async (
  dishName: string,
  dishDescription: string,
  ingredients: string[]
) => {
  try {
    const response = await axios.post("/suggest/get-recipe", {
      recipe: {
        name: dishName,
        description: dishDescription,
      },
      ingredients,
    });

    if (response.status !== 200) {
      console.log("Something went wrong while generating recipe");
    }

    return response.data;
  } catch (error) {
    console.log("Error in fullRecipe:", error);
    throw error;
  }
};
