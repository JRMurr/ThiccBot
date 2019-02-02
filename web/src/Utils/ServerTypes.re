type discordServer = {
  admin_role: option(int),
  command_prefixes: option(array(string)),
  id: string,
  name: string,
};

module ServerAPI = {
  let decodeServer = json =>
    Json.Decode.{
      admin_role: json |> field("admin_role", optional(int)),
      command_prefixes:
        json |> field("command_prefixes", optional(array(string))),
      id: json |> field("id", string),
      name: json |> field("name", string),
    };

  let decodeAllServers = Json.Decode.array(decodeServer);

  let getServers = () =>
    ApiUtil.getJson(~route="api/servers", ~decoder=decodeAllServers);

  let getServer = id =>
    ApiUtil.getJson(~route="api/servers/" ++ id, ~decoder=decodeServer);
};