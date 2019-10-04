let basePath = "http://localhost:4000";

let join_route = route => {
  switch (route.[0]) {
  | '/' => basePath ++ route
  | _ =>
    let x = String.concat("/", [basePath, route]);
    Js.log(x);
    x;
  };
};

let getJson = (~route: string, ~decoder) =>
  Js.Promise.(
    Fetch.fetch(join_route(route))
    |> then_(Fetch.Response.json)
    |> then_(json => decoder(json) |> resolve)
  );