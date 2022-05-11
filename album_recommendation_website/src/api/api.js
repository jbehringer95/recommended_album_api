export const fetchTags = async () => {
  try {
    const response = await fetch(
      `http://recommended-album-api-dev.us-east-1.elasticbeanstalk.com/tags`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.json();
  } catch (error) {
    return error;
  }
};

export const fetchRecommendedAlbum = async ({ searchQuery }) => {
  try {
    const response = await fetch(
      // `http://recommended-album-api-dev.us-east-1.elasticbeanstalk.com/prediction/%5B%27thrash%20Metal%27,%20%27Acoustic%20rock%27,%20%27ENErgetic%27,%20%27Male%20VocaLs%27,%20%27alternative%20rock%27,%20%27Art%20Rock%27,%20%27melancholic%27%5D`,
      `http://recommended-album-api-dev.us-east-1.elasticbeanstalk.com/prediction/${searchQuery}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.json();
  } catch (error) {
    return error;
  }
};
