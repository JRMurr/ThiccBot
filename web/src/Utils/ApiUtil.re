let basePath = "http://localhost:4000";

let join_route = route => {
  switch (route.[0]) {
  | '/' => basePath ++ route
  | _ => String.concat("/", [basePath, route])
  };
};

let getJson = (~route: string, ~decoder) =>
  Js.Promise.(
    Fetch.fetch(join_route(route))
    |> then_(Fetch.Response.json)
    |> then_(json => decoder(json) |> resolve)
  );