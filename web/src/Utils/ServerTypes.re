[@decco]
type discordServer = {
  admin_role: option(string),
  command_prefixes: option(array(string)),
  message_prefixes: option(array(string)),
  id: string,
  server_group_id: string,
  name: string,
};

module ServerAPI = {
  // let decodeServer = json =>
  //   Json.Decode.{
  //     admin_role: json |> field("admin_role", optional(string)),
  //     command_prefixes:
  //       json |> field("command_prefixes", optional(array(string))),
  //     message_prefixes:
  //       json |> field("message_prefixes", optional(array(string))),
  //     id: json |> field("id", string),
  //     server_group_id: json |> field("server_group_id", string),
  //     name: json |> field("name", string),
  //   };
  let decodeServer = json => discordServer_decode(json) |> Belt.Result.getExn;

  let decodeAllServers = Json.Decode.array(decodeServer);

  let getServers = () =>
    ApiUtil.getJson(~route="api/discord", ~decoder=decodeAllServers);

  let getServer = id =>
    ApiUtil.getJson(~route="api/discord/" ++ id, ~decoder=decodeServer);
};