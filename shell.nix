{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
  pythonEnv = python35.withPackages (ps: [
    ps.requests
    ps.flask
    ps.pyyaml
  ]);
in mkShell {
  buildInputs = [
    pythonEnv
  ];
}
